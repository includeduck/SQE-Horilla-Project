# Use Cases: Muhammad Wasay Tariq (24I-3071)

Two use cases per member (brief §2, browser end to end). Rayyan's use cases (`RAYYAN_USE_CASES.md`) cover the **employee** side of both workflows (requesting an allocation, requesting leave). These two cover the **approver** side, which the traceability matrix showed had no browser-level test (FR-02, FR-03, FR-08, FR-09, BR-03, BR-04).

Every flow below is automated in [`tests/team/e2e/test_wasay_use_cases.py`](../../tests/team/e2e/test_wasay_use_cases.py) (Python Playwright on the isolated Area 2 live-server fixtures) and runs in the CI gate's `e2e` job. Each test asserts what the screen shows **and** the postconditions through the API: request status, the requester's balance, and that the approver's and an unrelated employee's balances did not change.

Shared setup (fixtures in `tests/team/api/conftest.py`): company, leave type "Team Annual Leave", **employee** (`team_employee`, balance 0), **approver** (`team_approver`, the employee's reporting manager, own balance 7), **outsider** (`team_outsider`, unrelated, balance 9).

---

## UC-WAS-01: Approver decides a leave allocation request (W1)

| Field | Content |
|---|---|
| **Primary actor** | Leave Approver (the employee's reporting manager) |
| **Goal** | Grant or refuse extra leave days that an employee asked for |
| **Trigger** | An employee has submitted an allocation request |
| **Requirements** | FR-02, FR-03, BR-03 (state change), BR-04 (permission) |
| **Preconditions** | P1 the employee has a **requested** allocation request for **3** days of Team Annual Leave; P2 the employee's balance is 0; P3 the approver is logged in and is the employee's reporting manager |
| **Postconditions (success)** | The request is **approved** and the employee's balance is **3**, or it is **rejected** with the reason stored and the balance still **0**. Approver (7) and outsider (9) balances unchanged |
| **Postconditions (failure)** | The request stays **requested**, all balances unchanged |

**Main flow (MAIN): approve**
1. Approver opens *Leave → Leave Allocation Request* and selects the **Leave Allocation Requests** tab (requests of the people they manage).
2. The system lists the employee's request with status *Requested*.
3. Approver clicks **Approve** on the request.
4. The system asks "Do you want to approve this request?".
5. Approver confirms.
6. The system credits 3 days to the employee's balance, marks the request **approved** and shows "Leave allocation request approved successfully".

**Alternative flows**
- **A1: reject with a reason.** At step 3 the approver clicks **Reject**, the system shows a reason form, the approver enters a reason and submits. The system marks the request **rejected**, stores the reason, leaves the balance at 0 and shows "Leave allocation request rejected successfully".
- **A2: change of mind at the confirmation.** At step 5 the approver dismisses the dialog. Nothing changes (still requested, balance 0). The approver clicks **Approve** again and confirms; the flow continues at step 6.

**Exception flows**
- **E1: reject without a reason.** In A1 the approver submits the form with the reason empty. The form is not sent: the browser marks the required *Reason* field. The request stays requested, the balance 0.
- **E2: the employee tries to approve their own request.** The employee (not an approver) opens the approve link for their own request. The system refuses with "You don't have permission"; the request stays requested and no days are credited.

---

## UC-WAS-02: Approver decides a leave request (W2)

| Field | Content |
|---|---|
| **Primary actor** | Leave Approver (the employee's reporting manager) |
| **Goal** | Approve or refuse an employee's leave, including reversing an earlier approval |
| **Trigger** | An employee has submitted a leave request |
| **Requirements** | FR-08, FR-09, BR-03 (state change), BR-04 (permission) |
| **Preconditions** | P1 the employee's balance is **5** (granted through W1); P2 the employee has a **requested** leave request of *d* working days (*d* < 5); P3 the approver is logged in and is the employee's reporting manager |
| **Postconditions (success)** | Approved: status **approved**, employee balance **5 − d**. Rejected: status **rejected**, reason stored, employee balance **5** (refunded if it had been approved). Approver (7) and outsider (9) balances unchanged in every case |
| **Postconditions (failure)** | The request keeps its status, all balances unchanged |

**Main flow (MAIN): approve**
1. Approver opens *Leave → Leave Requests*.
2. The system lists the employee's request with status *Requested*.
3. Approver clicks **Approve** on the request.
4. The system asks for confirmation.
5. Approver confirms.
6. The system deducts *d* days from the employee's balance, marks the request **approved** and shows "Leave request approved successfully".

**Alternative flows**
- **A1: reject a requested leave with a reason.** At step 3 the approver clicks **Reject**, enters a reason and submits. The system marks the request **rejected**, stores the reason and shows "Leave request rejected successfully"; the balance stays 5 (nothing had been deducted).
- **A2: reverse an approved leave.** The request was approved earlier (balance 5 − d). The approver clicks **Reject** on it, enters a reason and submits. The system marks it **rejected** and **refunds the d days to the employee** (balance 5); the approver's own balance is untouched (regression for defect #4).

**Exception flows**
- **E1: reject without a reason.** The approver submits the reject form with the reason empty. The form is not sent (required field); the request stays requested, balance 5.
- **E2: the employee tries to approve their own leave.** The employee opens the approve link for their own request. The system refuses with an error message; the request stays requested and the balance stays 5.

---

## Traceability of the flows

| Test (pytest id) | Flow | Requirements |
|---|---|---|
| `test_uc_was_01_allocation_decision[UC-WAS-01-MAIN]` | approve | FR-02, FR-10, BR-03, BR-04 |
| `…[UC-WAS-01-A1]` | reject with reason | FR-03, BR-03 |
| `…[UC-WAS-01-A2]` | dismiss, then approve | FR-02, BR-03 |
| `…[UC-WAS-01-E1]` | reject without reason refused | FR-03, BR-03 |
| `…[UC-WAS-01-E2]` | employee self-approval denied | BR-04 |
| `test_uc_was_02_leave_decision[UC-WAS-02-MAIN]` | approve | FR-08, FR-10, BR-03, BR-04 |
| `…[UC-WAS-02-A1]` | reject requested | FR-09, BR-03 |
| `…[UC-WAS-02-A2]` | reverse an approval, refund to requester | FR-09, BR-01, BR-03 |
| `…[UC-WAS-02-E1]` | reject without reason refused | FR-09, BR-03 |
| `…[UC-WAS-02-E2]` | employee self-approval denied | BR-04 |
