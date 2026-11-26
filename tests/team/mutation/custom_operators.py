"""Custom mutation operators derived from the leave business rules.

mutmut's built-in operators are generic (swap `<` and `<=`, change numbers,
mangle strings to "XXabcXX", ...). These three model the mistakes a developer is
likely to make in *this* domain:

  BR-03  leave_state_swap      Use the wrong state of the leave state machine
                               ("approved" where "requested" was meant, ...).
  BR-01  balance_term_drop     Forget one component of a leave-day sum
                               (available + carry-forward + forecast).
  BR-01  day_breakdown_swap    Use the wrong half-day breakdown
                               ("first_half" where "full_day" was meant, ...).

Each operator receives a libcst node and yields mutated replacement nodes, the
same contract as mutmut.mutation.mutators.mutation_operators.
"""

import libcst as cst

# BR-03: each state is replaced by the state a developer most plausibly confuses
# it with (its neighbour in the state machine), one mutant per literal.
STATE_NEIGHBOUR = {
    "requested": "approved",
    "approved": "requested",
    "rejected": "cancelled",
    "cancelled": "rejected",
    "cancel_requested": "approved",
}

# BR-01: day-unit confusion between full and half days.
BREAKDOWN_SWAP = {
    "full_day": "first_half",
    "first_half": "second_half",
    "second_half": "first_half",
}


def _swap_literal(node: cst.SimpleString, mapping: dict):
    quote = node.value[0]
    inner = node.value[1:-1]
    if node.prefix or inner not in mapping:
        return
    yield node.with_changes(value=f"{quote}{mapping[inner]}{quote}")


def leave_state_swap(node: cst.SimpleString):
    """BR-03: replace a leave/allocation state literal with a neighbouring state."""
    yield from _swap_literal(node, STATE_NEIGHBOUR)


def day_breakdown_swap(node: cst.SimpleString):
    """BR-01: replace a day-breakdown literal with a different breakdown."""
    yield from _swap_literal(node, BREAKDOWN_SWAP)


def _is_days_term(expr: cst.BaseExpression) -> bool:
    if isinstance(expr, cst.Name):
        return "days" in expr.value
    if isinstance(expr, cst.Attribute):
        return "days" in expr.attr.value
    if isinstance(expr, cst.BinaryOperation):
        return _is_days_term(expr.left) or _is_days_term(expr.right)
    return False


def balance_term_drop(node: cst.BinaryOperation):
    """BR-01: in `a + b` / `a - b` over leave-day quantities, drop one term."""
    if not isinstance(node.operator, (cst.Add, cst.Subtract)):
        return
    if not (_is_days_term(node.left) or _is_days_term(node.right)):
        return
    yield node.left.with_changes(lpar=[cst.LeftParen()], rpar=[cst.RightParen()])
    yield node.right.with_changes(lpar=[cst.LeftParen()], rpar=[cst.RightParen()])


CUSTOM_OPERATORS = [
    (cst.SimpleString, leave_state_swap),
    (cst.SimpleString, day_breakdown_swap),
    (cst.BinaryOperation, balance_term_drop),
]
