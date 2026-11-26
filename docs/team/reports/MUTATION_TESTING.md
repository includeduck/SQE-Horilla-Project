# Mutation Testing (Area 1)

Owner: Muhammad Wasay Tariq (24I-3071). Brief §2: "Run a mutation tool on the business-rule module and report the score. Add at least 2 custom mutation operators based on your business rules. Analyse at least 15 surviving mutants (equivalent, missing test or weak assertion) and kill the killable ones."

## 1. Setup

| Item | Value |
|---|---|
| Tool | **mutmut 3.8.1** (Python), run in WSL Ubuntu 26.04 (mutmut needs POSIX `fork()`) |
| Python / Django | 3.12 / 5.2.19, same `requirements.txt` as the app |
| Code | `sqe-team` @ `1c25674bb` (includes the PR #8 defect fixes) |
| Config | [`setup.cfg`](../../../setup.cfg) `[mutmut]`; runner [`tests/team/mutation/run_mutmut.py`](../../../tests/team/mutation/run_mutmut.py) |
| Tests used | `tests/team/unit` (Area 1 unit suite, in-memory SQLite) |
| Business-rule module | `leave/models.py`, `leave/methods.py`, `horilla_api/api_views/leave/views.py`, narrowed to the **15 scoped functions** in [`coverage_scope.py`](../../../tests/team/unit/coverage_scope.py); `mutate_only_covered_lines = true` |
| Run time | about 4 minutes for 475 mutants (12 cores, forked workers) |

```bash
# WSL, repo root, project venv
python tests/team/mutation/run_mutmut.py run            # scoped run with custom operators
python tests/team/mutation/analyse.py --out docs/team/evidence/mutation/runN
python tests/team/mutation/run_mutmut.py show <mutant>  # diff of one mutant
```

**Tool limitation:** mutmut 3 does not mutate decorated functions, so the three `put` methods wrapped by `@approver_permission_required` (`LeaveRequestRejectAPIView.put`, `LeaveAllocationApproveAPIView.put`, `LeaveAllocationRequestRejectAPIView.put`) produce no mutants. They mostly delegate to the mutated `*_calculation` methods and stay at 100% statement/branch coverage in the unit tests.

## 2. Custom mutation operators (business rules)

mutmut has no plugin API, so [`run_mutmut.py`](../../../tests/team/mutation/run_mutmut.py) appends three operators from [`custom_operators.py`](../../../tests/team/mutation/custom_operators.py) to mutmut's own operator list (`mutmut.mutation.mutators.mutation_operators`) before starting mutmut's CLI. They run inside the tool exactly like the built-in operators.

| Operator | Rule | What it does | Example | Mutants | Killed (run 1 / run 2) |
|---|---|---|---|---|---|
| `leave_state_swap` | BR-03 | Replaces a state literal with its neighbour in the state machine (`requested`↔`approved`, `rejected`↔`cancelled`, `cancel_requested`→`approved`) | `status == "requested"` → `status == "approved"` | 7 | 7 / 7 |
| `balance_term_drop` | BR-01 | Drops one term from a `+`/`-` over leave-day quantities | `available + carry + forecast` → `(available + carry)` | 23 | 22 / **23** |
| `day_breakdown_swap` | BR-01 | Swaps half-day breakdown literals (`full_day`→`first_half`→`second_half`→`first_half`) | `== "full_day"` → `== "first_half"` | 6 | 6 / 6 |

They model mistakes specific to this domain that the built-in operators miss: mutmut's string operator only produces `"XXrequestedXX"`, which any test kills, never a *valid but wrong* state.

## 3. Results

| Run | Unit tests | Mutants | Killed | Survived | Score |
|---|---|---|---|---|---|
| 1: baseline | 127 | 475 | 404 | 71 | **85.1%** |
| 2: after survivor analysis | 159 (+32 in `test_mutation_killers.py`) | 475 | 465 | 10 | **97.9%** |
| 2, excluding the 10 equivalent mutants | | 465 | 465 | 0 | **100%** |

Per function, run 1 → run 2:

| Function | Run 1 killed/total | Run 2 killed/total |
|---|---|---|
| `calculate_requested_days` | 44/44 | 44/44 |
| `leave_requested_dates` | 10/10 | 10/10 |
| `cal_effective_requested_days` | 50/54 | 54/54 |
| `AvailableLeave.forcasted_leaves` | 12/12 | 12/12 |
| `LeaveRequest.leaveoverlapping` | 21/24 | 24/24 |
| `LeaveRequest.clean` (critical module) | 196/243 | 234/243 (9 equivalent) |
| `LeaveAllocationRequest.clean` | 7/9 | 9/9 |
| `LeaveRequestApproveAPIView.leave_approve_calculation` | 18/19 | 18/19 (1 equivalent) |
| `LeaveRequestRejectAPIView.leave_calculation` | 15/18 | 18/18 |
| `LeaveAllocationApproveAPIView.approve_calculations` | 8/8 | 8/8 |
| `LeaveAllocationRequestRejectAPIView.reject_calculation` | 18/20 | 20/20 |
| `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` | 5/14 | 14/14 |

Evidence: [`evidence/mutation/run1-baseline/`](../evidence/mutation/run1-baseline/) and [`run2-after-killers/`](../evidence/mutation/run2-after-killers/) (`summary.json`, and every survivor with its diff in `survivors.md`).

**What 100% coverage did not catch.** The suite already had 100% statement and branch coverage, yet 61 non-equivalent mutants survived run 1. Coverage shows that a line ran; mutation testing shows whether any test would notice the line being wrong.

## 4. Analysis of all 71 surviving mutants (run 1)

| Category | Count | Meaning | Action |
|---|---|---|---|
| **Equivalent** | 10 | No input can tell the mutant from the original | Justified in §5; left alive |
| **Weak assertion** | 31 | The code ran and the outcome was checked, but not precisely (e.g. `match="not assigned"` instead of the exact message and field key) | Exact message and field-key assertions |
| **Missing test** | 30 | No test created the situation that tells them apart (query filters, `or 0` defaults, the forecast term, `continue` vs `break` with two restrictions) | New scenario tests |

Main lessons:
- **Query filters were untested.** Removing `employee_id=` or `leave_type_id=` from a lookup survived because each test had only one balance row. Tests now add rows for another employee and another leave type, so a missing filter picks the wrong row (S10, S11, S13, S14, S25, S26, S45, S46, S70).
- **The forecast term of BR-01 was never non-zero.** `forcasted_days` was always 0, so dropping it (custom `balance_term_drop`, S61) or negating it (S60) survived. `test_forecast_of_next_reset_counts_towards_balance` uses a leave type that resets daily.
- **`or 0` defaults.** `available_days or 0` → `or 1` survived because no test had a zero balance with a one-day request (S57–S59).
- **Error messages and field keys** are part of the API contract the client shows; substring matches let `"XX…XX"` and case changes through.

Full table (generated from the run 1 data; killing tests are in `tests/team/unit/test_mutation_killers.py`):

| # | Function | Mutation | Category | Reason / killing test | Run 2 |
|---|---|---|---|---|---|
| S01 | `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` | `raise Http404("AnonymousUser") → raise Http404(None)` | Weak assertion | `test_exact_ownership_errors` | killed |
| S02 | `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` | `raise Http404("AnonymousUser") → raise Http404("XXAnonymousUserXX")` | Weak assertion | `test_exact_ownership_errors` | killed |
| S03 | `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` | `raise Http404("AnonymousUser") → raise Http404("anonymoususer")` | Weak assertion | `test_exact_ownership_errors` | killed |
| S04 | `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` | `raise Http404("AnonymousUser") → raise Http404("ANONYMOUSUSER")` | Weak assertion | `test_exact_ownership_errors` | killed |
| S05 | `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` | `raise PermissionDenied(_("Access Denied..")) → raise PermissionDenied(None)` | Weak assertion | `test_exact_ownership_errors` | killed |
| S06 | `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` | `raise PermissionDenied(_("Access Denied..")) → raise PermissionDenied(_("XXAccess Denied..XX"))` | Weak assertion | `test_exact_ownership_errors` | killed |
| S07 | `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` | `raise PermissionDenied(_("Access Denied..")) → raise PermissionDenied(_("access denied.."))` | Weak assertion | `test_exact_ownership_errors` | killed |
| S08 | `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` | `raise PermissionDenied(_("Access Denied..")) → raise PermissionDenied(_("ACCESS DENIED.."))` | Weak assertion | `test_exact_ownership_errors` | killed |
| S09 | `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` | `raise serializers.ValidationError(e) → raise serializers.ValidationError(None)` | Weak assertion | `test_exact_ownership_errors` | killed |
| S10 | `LeaveAllocationRequestRejectAPIView.reject_calculation` | `leave_type_id=leave_type,` | Missing test | `test_reject_approved_allocation_debits_only_matching_row` | killed |
| S11 | `LeaveAllocationRequestRejectAPIView.reject_calculation` | `employee_id=leave_allocation_request.employee_id, → ).first()` | Missing test | `test_reject_approved_allocation_debits_only_matching_row` | killed |
| S12 | `LeaveRequestApproveAPIView.leave_approve_calculation` | `if leave_request.requested_days > available_leave.avail → if leave_request.requested_days >= available_leave.avai` | Equivalent | At requested == available both branches give the same result (available 0, approved_available = requested, carry unchanged, approved_carry 0). | survived (equivalent) |
| S13 | `LeaveRequestRejectAPIView.leave_calculation` | `leave_type_id=leave_type_id, employee_id=employee_id → employee_id=employee_id` | Missing test | `test_reject_leave_refunds_only_matching_row` | killed |
| S14 | `LeaveRequestRejectAPIView.leave_calculation` | `leave_type_id=leave_type_id, employee_id=employee_id → )` | Missing test | `test_reject_leave_refunds_only_matching_row` | killed |
| S15 | `LeaveRequestRejectAPIView.leave_calculation` | `available_leave.carryforward_days += leave_request.appr → available_leave.carryforward_days = leave_request.appro` | Missing test | `test_reject_leave_refunds_only_matching_row` | killed |
| S16 | `cal_effective_requested_days` | `Q(is_specific=False) \| Q(employees=employee) → Q(is_specific=False) \| Q(employees=None)` | Missing test | `test_specific_holiday_of_this_employee_is_excluded` | killed |
| S17 | `cal_effective_requested_days` | `company_leave_dates_list(CompanyLeaves.objects.all(), s → company_leave_dates_list(CompanyLeaves.objects.all(), s` | Missing test | `test_company_leave_dates_called_with_request_range` | killed |
| S18 | `cal_effective_requested_days` | `company_leave_dates_list(CompanyLeaves.objects.all(), s → company_leave_dates_list(CompanyLeaves.objects.all(), e` | Missing test | `test_company_leave_dates_called_with_request_range` | killed |
| S19 | `cal_effective_requested_days` | `company_leave_dates_list(CompanyLeaves.objects.all(), s → company_leave_dates_list(CompanyLeaves.objects.all(), s` | Missing test | `test_company_leave_dates_called_with_request_range` | killed |
| S20 | `LeaveAllocationRequest.clean` | `"This form cannot be edited because the status is Reque → "XXThis form cannot be edited because the status is Req` | Weak assertion | `test_exact_allocation_edit_lock_message` | killed |
| S21 | `LeaveAllocationRequest.clean` | `"This form cannot be edited because the status is Reque → "this form cannot be edited because the status is reque` | Weak assertion | `test_exact_allocation_edit_lock_message` | killed |
| S22 | `LeaveRequest.clean` | `cleaned_data = super().clean() → cleaned_data = None` | Equivalent | Model.clean() returns None, so cleaned_data is None either way. | survived (equivalent) |
| S23 | `LeaveRequest.clean` | `attachment = getattr(self, "attachment", None) → attachment = getattr(self, "attachment", )` | Equivalent | `attachment` is a model field, so getattr never needs the default. | survived (equivalent) |
| S24 | `LeaveRequest.clean` | `request = getattr(horilla_middlewares._thread_locals, " → request = getattr(horilla_middlewares._thread_locals, "` | Equivalent | Without a request both versions fail at `request.user` (AttributeError). | survived (equivalent) |
| S25 | `LeaveRequest.clean` | `employee_id=self.employee_id, leave_type_id=leave_type → leave_type_id=leave_type` | Missing test | `test_not_assigned_even_if_other_rows_exist` | killed |
| S26 | `LeaveRequest.clean` | `employee_id=self.employee_id, leave_type_id=leave_type → ).exists():` | Missing test | `test_not_assigned_even_if_other_rows_exist` | killed |
| S27 | `LeaveRequest.clean` | `"leave_type_id": _( → "XXleave_type_idXX": _(` | Weak assertion | `test_exact_not_assigned_message_and_field` | killed |
| S28 | `LeaveRequest.clean` | `"leave_type_id": _( → "LEAVE_TYPE_ID": _(` | Weak assertion | `test_exact_not_assigned_message_and_field` | killed |
| S29 | `LeaveRequest.clean` | `"The selected leave type is not assigned to this employ → "XXThe selected leave type is not assigned to this empl` | Weak assertion | `test_exact_not_assigned_message_and_field` | killed |
| S30 | `LeaveRequest.clean` | `"The selected leave type is not assigned to this employ → "the selected leave type is not assigned to this employ` | Weak assertion | `test_exact_not_assigned_message_and_field` | killed |
| S31 | `LeaveRequest.clean` | `raise ValidationError(_("End date should not be less th → raise ValidationError(_("XXEnd date should not be less ` | Weak assertion | `test_exact_end_before_start_message` | killed |
| S32 | `LeaveRequest.clean` | `_("Mismatch in the breakdown of the start and end date. → _("XXMismatch in the breakdown of the start and end dat` | Weak assertion | `test_exact_breakdown_mismatch_message` | killed |
| S33 | `LeaveRequest.clean` | `{"attachment": _("An attachment is required for this le → {"XXattachmentXX": _("An attachment is required for thi` | Weak assertion | `test_exact_attachment_message_and_field` | killed |
| S34 | `LeaveRequest.clean` | `{"attachment": _("An attachment is required for this le → {"ATTACHMENT": _("An attachment is required for this le` | Weak assertion | `test_exact_attachment_message_and_field` | killed |
| S35 | `LeaveRequest.clean` | `{"attachment": _("An attachment is required for this le → {"attachment": _("XXAn attachment is required for this ` | Weak assertion | `test_exact_attachment_message_and_field` | killed |
| S36 | `LeaveRequest.clean` | `{"attachment": _("An attachment is required for this le → {"attachment": _("an attachment is required for this le` | Weak assertion | `test_exact_attachment_message_and_field` | killed |
| S37 | `LeaveRequest.clean` | `if self.start_date and self.end_date: → if self.start_date or self.end_date:` | Equivalent | Both dates are always set here (a None end date already raises at line 2069). | survived (equivalent) |
| S38 | `LeaveRequest.clean` | `overlapping_requests = self.leaveoverlapping().exclude( → overlapping_requests = self.leaveoverlapping().exclude(` | Equivalent | leaveoverlapping() already excludes self.id; the second exclude is redundant. | survived (equivalent) |
| S39 | `LeaveRequest.clean` | `_("Employee already has a leave request for this date r → _("XXEmployee already has a leave request for this date` | Weak assertion | `test_exact_overlap_message` | killed |
| S40 | `LeaveRequest.clean` | `_("Employee already has a leave request for this date r → _("employee already has a leave request for this date r` | Weak assertion | `test_exact_overlap_message` | killed |
| S41 | `LeaveRequest.clean` | `enabled=True, company_id=emp_company → company_id=emp_company` | Missing test | `test_disabled_past_date_restriction_is_ignored` | killed |
| S42 | `LeaveRequest.clean` | `enabled=True, company_id=emp_company → ).first()` | Missing test | `test_past_date_restriction_of_other_company_is_ignored` | killed |
| S43 | `LeaveRequest.clean` | `raise ValidationError(_("Requests cannot be made for pa → raise ValidationError(_("XXRequests cannot be made for ` | Weak assertion | `test_exact_past_date_message` | killed |
| S44 | `LeaveRequest.clean` | `raise ValidationError(_("Requests cannot be made for pa → raise ValidationError(_("requests cannot be made for pa` | Weak assertion | `test_exact_past_date_message` | killed |
| S45 | `LeaveRequest.clean` | `employee_id=self.employee_id, leave_type_id=leave_type → leave_type_id=leave_type` | Missing test | `test_balance_lookup_uses_employee_and_type` | killed |
| S46 | `LeaveRequest.clean` | `employee_id=self.employee_id, leave_type_id=leave_type → )` | Missing test | `test_balance_lookup_uses_employee_and_type` | killed |
| S47 | `LeaveRequest.clean` | `self.end_date_breakdown, → None,` | Missing test | `test_end_breakdown_is_passed_to_day_count` | killed |
| S48 | `LeaveRequest.clean` | `end_date=self.end_date, → end_date=None,` | Missing test | `test_end_date_is_passed_to_effective_day_count` | killed |
| S49 | `LeaveRequest.clean` | `employee=self.employee_id, → employee=None,` | Missing test | `test_specific_holiday_of_other_employee_is_not_excluded` | killed |
| S50 | `LeaveRequest.clean` | `employee=self.employee_id, → )` | Missing test | `test_specific_holiday_of_other_employee_is_not_excluded` | killed |
| S51 | `LeaveRequest.clean` | `"The requested days for this leave type is zero. Please → "XXThe requested days for this leave type is zero. Plea` | Weak assertion | `test_exact_zero_days_message` | killed |
| S52 | `LeaveRequest.clean` | `"The requested days for this leave type is zero. Please → "the requested days for this leave type is zero. please` | Weak assertion | `test_exact_zero_days_message` | killed |
| S53 | `LeaveRequest.clean` | `leave_dates = leave_requested_dates(self.start_date, se → leave_dates = leave_requested_dates(self.start_date, No` | Equivalent | leave_dates only feeds dead code (month_year / unique_dates, issue #12). | survived (equivalent) |
| S54 | `LeaveRequest.clean` | `month_year = [f"{date.year}-{date.strftime('%m')}" for  → month_year = [f"{date.year}-{date.strftime('XX%mXX')}" ` | Equivalent | Dead code (issue #12). | survived (equivalent) |
| S55 | `LeaveRequest.clean` | `month_year = [f"{date.year}-{date.strftime('%m')}" for  → month_year = [f"{date.year}-{date.strftime('%M')}" for ` | Equivalent | Dead code (issue #12). | survived (equivalent) |
| S56 | `LeaveRequest.clean` | `forcated_days = available_leave.forcasted_leaves(self.s → forcated_days = available_leave.forcasted_leaves(None)` | Missing test | `test_forecast_of_next_reset_counts_towards_balance` | killed |
| S57 | `LeaveRequest.clean` | `available_days = available_leave.available_days or 0 → available_days = available_leave.available_days or 1` | Missing test | `test_balance_defaults_do_not_add_a_day (available 0)` | killed |
| S58 | `LeaveRequest.clean` | `carryforward_days = available_leave.carryforward_days o → carryforward_days = available_leave.carryforward_days o` | Missing test | `test_balance_defaults_do_not_add_a_day (carry 0)` | killed |
| S59 | `LeaveRequest.clean` | `carryforward_max = available_leave.leave_type_id.carryf → carryforward_max = available_leave.leave_type_id.carryf` | Missing test | `test_balance_defaults_do_not_add_a_day (carry max None)` | killed |
| S60 | `LeaveRequest.clean` | `total_leave_days = available_days + carryforward_days + → total_leave_days = available_days + carryforward_days -` | Missing test | `test_forecast_of_next_reset_counts_towards_balance` | killed |
| S61 | `LeaveRequest.clean` | `total_leave_days = available_days + carryforward_days + → total_leave_days = (available_days + carryforward_days)` (custom op) | Missing test | `test_forecast_of_next_reset_counts_towards_balance` | killed |
| S62 | `LeaveRequest.clean` | `_("Does not have sufficient leave balance for the reque → _("XXDoes not have sufficient leave balance for the req` | Weak assertion | `test_exact_insufficient_balance_message` | killed |
| S63 | `LeaveRequest.clean` | `_("Does not have sufficient leave balance for the reque → _("does not have sufficient leave balance for the reque` | Weak assertion | `test_exact_insufficient_balance_message` | killed |
| S64 | `LeaveRequest.clean` | `is_restricted = False → is_restricted = None` | Equivalent | None and False are both falsy for `if not is_restricted`. | survived (equivalent) |
| S65 | `LeaveRequest.clean` | `continue → break` | Missing test | `test_unrelated_restriction_does_not_stop_later_checks` | killed |
| S66 | `LeaveRequest.clean` | `continue → break` | Missing test | `test_empty_restriction_does_not_stop_later_checks` | killed |
| S67 | `LeaveRequest.clean` | `"You cannot request leave for this date range. The requ → "XXYou cannot request leave for this date range. The re` | Weak assertion | `test_exact_restricted_message` | killed |
| S68 | `LeaveRequest.clean` | `"You cannot request leave for this date range. The requ → "you cannot request leave for this date range. the requ` | Weak assertion | `test_exact_restricted_message` | killed |
| S69 | `LeaveRequest.leaveoverlapping` | `).exclude(id=self.id) → ).exclude(id=None)` | Missing test | `test_saved_request_does_not_overlap_itself` | killed |
| S70 | `LeaveRequest.leaveoverlapping` | `employee_id=self.employee_id,` | Missing test | `test_other_employees_request_is_not_an_overlap` | killed |
| S71 | `LeaveRequest.leaveoverlapping` | `start_date__lte=self.end_date,` | Missing test | `test_existing_request_after_new_end_is_not_an_overlap` | killed |

## 5. Equivalent mutants (why they cannot be killed)

| Mutant | Why it is equivalent |
|---|---|
| `leave_approve_calculation` `>` to `>=` | At requested == available, the "spill into carry-forward" branch computes `leave = 0`, so both branches end with available 0, approved_available = requested, carry unchanged, approved_carry 0. |
| `clean` `cleaned_data = None` | `Model.clean()` returns `None` anyway. |
| `clean` `getattr(self, "attachment", )` | `attachment` is a model field, so the default is never used. |
| `clean` `getattr(..., "request", )` | Without a request both versions fail at `request.user`. |
| `clean` `start_date and end_date` to `or` | Both dates are always set at this point (a `None` end date raises at line 2069, issue #11). |
| `clean` `.exclude(id=None)` after `leaveoverlapping()` | `leaveoverlapping()` already excludes `self.id`; the second exclude is redundant. |
| `clean` `leave_requested_dates(..., None)` and the two `strftime` mutants | They only feed `month_year` / `unique_dates`, which is dead code (issue #12). |
| `clean` `is_restricted = None` | `None` and `False` behave the same in `if not is_restricted`. |

Four of the ten exist only because of the dead code reported in #12; deleting that code would delete those mutants.

## 6. Inputs for the CI quality gate

- Proposed mutation threshold: **95%** on the scoped functions. Run 2 reaches 97.9% with every non-equivalent mutant killed, so 95% tolerates a few new equivalent mutants while still failing if a new rule arrives untested (the forecast gap alone was 3 mutants).
- A new survivor in a pull request must be killed or added to §5 with a reason.
