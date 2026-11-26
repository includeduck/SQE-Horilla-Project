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

Totals: {'Equivalent': 10, 'Weak assertion': 31, 'Missing test': 30}
