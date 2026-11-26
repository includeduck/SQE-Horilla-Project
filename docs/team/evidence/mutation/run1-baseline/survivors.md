# Surviving mutants (71)

Score 85.1% (404 killed / 475).

## S01 `horilla_api.api_views.leave.views.xǁEmployeeLeaveAllocationUpdateDeleteAPIViewǁget_allocation_request__mutmut_2`

Function: `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request`. Operator: built-in: '"An'->'N' | 'ymousUs'->'' | 'r"'->''

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -1,7 +1,7 @@
 def get_allocation_request(self, request, pk):
     user = request.user
     if isinstance(user, AnonymousUser):
-        raise Http404("AnonymousUser")
+        raise Http404(None)
     try:
         allocation_request = LeaveAllocationRequest.objects.get(id=pk)
         if allocation_request.employee_id == user.employee_get:
```

## S02 `horilla_api.api_views.leave.views.xǁEmployeeLeaveAllocationUpdateDeleteAPIViewǁget_allocation_request__mutmut_3`

Function: `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -1,7 +1,7 @@
 def get_allocation_request(self, request, pk):
     user = request.user
     if isinstance(user, AnonymousUser):
-        raise Http404("AnonymousUser")
+        raise Http404("XXAnonymousUserXX")
     try:
         allocation_request = LeaveAllocationRequest.objects.get(id=pk)
         if allocation_request.employee_id == user.employee_get:
```

## S03 `horilla_api.api_views.leave.views.xǁEmployeeLeaveAllocationUpdateDeleteAPIViewǁget_allocation_request__mutmut_4`

Function: `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request`. Operator: built-in: 'A'->'a' | 'U'->'u'

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -1,7 +1,7 @@
 def get_allocation_request(self, request, pk):
     user = request.user
     if isinstance(user, AnonymousUser):
-        raise Http404("AnonymousUser")
+        raise Http404("anonymoususer")
     try:
         allocation_request = LeaveAllocationRequest.objects.get(id=pk)
         if allocation_request.employee_id == user.employee_get:
```

## S04 `horilla_api.api_views.leave.views.xǁEmployeeLeaveAllocationUpdateDeleteAPIViewǁget_allocation_request__mutmut_5`

Function: `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request`. Operator: built-in: 'nonymous'->'NONYMO' | 'ser'->'SUSER'

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -1,7 +1,7 @@
 def get_allocation_request(self, request, pk):
     user = request.user
     if isinstance(user, AnonymousUser):
-        raise Http404("AnonymousUser")
+        raise Http404("ANONYMOUSUSER")
     try:
         allocation_request = LeaveAllocationRequest.objects.get(id=pk)
         if allocation_request.employee_id == user.employee_get:
```

## S05 `horilla_api.api_views.leave.views.xǁEmployeeLeaveAllocationUpdateDeleteAPIViewǁget_allocation_request__mutmut_9`

Function: `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request`. Operator: built-in: '_("Acc'->'Non' | 'ss Denied.."'->'' | ')'->''

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -6,6 +6,6 @@
         allocation_request = LeaveAllocationRequest.objects.get(id=pk)
         if allocation_request.employee_id == user.employee_get:
             return allocation_request
-        raise PermissionDenied(_("Access Denied.."))
+        raise PermissionDenied(None)
     except LeaveAllocationRequest.DoesNotExist as e:
         raise serializers.ValidationError(e)
```

## S06 `horilla_api.api_views.leave.views.xǁEmployeeLeaveAllocationUpdateDeleteAPIViewǁget_allocation_request__mutmut_11`

Function: `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -6,6 +6,6 @@
         allocation_request = LeaveAllocationRequest.objects.get(id=pk)
         if allocation_request.employee_id == user.employee_get:
             return allocation_request
-        raise PermissionDenied(_("Access Denied.."))
+        raise PermissionDenied(_("XXAccess Denied..XX"))
     except LeaveAllocationRequest.DoesNotExist as e:
         raise serializers.ValidationError(e)
```

## S07 `horilla_api.api_views.leave.views.xǁEmployeeLeaveAllocationUpdateDeleteAPIViewǁget_allocation_request__mutmut_12`

Function: `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request`. Operator: built-in: 'A'->'a' | 'D'->'d'

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -6,6 +6,6 @@
         allocation_request = LeaveAllocationRequest.objects.get(id=pk)
         if allocation_request.employee_id == user.employee_get:
             return allocation_request
-        raise PermissionDenied(_("Access Denied.."))
+        raise PermissionDenied(_("access denied.."))
     except LeaveAllocationRequest.DoesNotExist as e:
         raise serializers.ValidationError(e)
```

## S08 `horilla_api.api_views.leave.views.xǁEmployeeLeaveAllocationUpdateDeleteAPIViewǁget_allocation_request__mutmut_13`

Function: `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request`. Operator: built-in: 'ccess'->'CCESS' | 'enied'->'ENIED'

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -6,6 +6,6 @@
         allocation_request = LeaveAllocationRequest.objects.get(id=pk)
         if allocation_request.employee_id == user.employee_get:
             return allocation_request
-        raise PermissionDenied(_("Access Denied.."))
+        raise PermissionDenied(_("ACCESS DENIED.."))
     except LeaveAllocationRequest.DoesNotExist as e:
         raise serializers.ValidationError(e)
```

## S09 `horilla_api.api_views.leave.views.xǁEmployeeLeaveAllocationUpdateDeleteAPIViewǁget_allocation_request__mutmut_14`

Function: `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request`. Operator: built-in: ''->'Non'

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -8,4 +8,4 @@
             return allocation_request
         raise PermissionDenied(_("Access Denied.."))
     except LeaveAllocationRequest.DoesNotExist as e:
-        raise serializers.ValidationError(e)
+        raise serializers.ValidationError(None)
```

## S10 `horilla_api.api_views.leave.views.xǁLeaveAllocationRequestRejectAPIViewǁreject_calculation__mutmut_10`

Function: `LeaveAllocationRequestRejectAPIView.reject_calculation`. Operator: built-in: '            leave_type_id=leave_type,'->''

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -3,7 +3,6 @@
         leave_type = leave_allocation_request.leave_type_id
         requested_days = leave_allocation_request.requested_days
         available_leave = AvailableLeave.objects.filter(
-            leave_type_id=leave_type,
             employee_id=leave_allocation_request.employee_id,
         ).first()
         available_leave.available_days = max(
```

## S11 `horilla_api.api_views.leave.views.xǁLeaveAllocationRequestRejectAPIViewǁreject_calculation__mutmut_11`

Function: `LeaveAllocationRequestRejectAPIView.reject_calculation`. Operator: built-in: '        employee_id=leave_allocation_request.employee_id,\n'->''

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -4,8 +4,7 @@
         requested_days = leave_allocation_request.requested_days
         available_leave = AvailableLeave.objects.filter(
             leave_type_id=leave_type,
-            employee_id=leave_allocation_request.employee_id,
-        ).first()
+            ).first()
         available_leave.available_days = max(
             0, available_leave.available_days - requested_days
         )
```

## S12 `horilla_api.api_views.leave.views.xǁLeaveRequestApproveAPIViewǁleave_approve_calculation__mutmut_1`

Function: `LeaveRequestApproveAPIView.leave_approve_calculation`. Operator: built-in: ''->'='

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -1,5 +1,5 @@
 def leave_approve_calculation(self, leave_request, available_leave):
-    if leave_request.requested_days > available_leave.available_days:
+    if leave_request.requested_days >= available_leave.available_days:
         leave = leave_request.requested_days - available_leave.available_days
         leave_request.approved_available_days = available_leave.available_days
         available_leave.available_days = 0
```

## S13 `horilla_api.api_views.leave.views.xǁLeaveRequestRejectAPIViewǁleave_calculation__mutmut_5`

Function: `LeaveRequestRejectAPIView.leave_calculation`. Operator: built-in: ' leave_type_id=leave_type_id,'->''

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -1,7 +1,7 @@
 def leave_calculation(self, leave_request, employee_id):
     leave_type_id = leave_request.leave_type_id
     available_leave = AvailableLeave.objects.get(
-        leave_type_id=leave_type_id, employee_id=employee_id
+        employee_id=employee_id
     )
     available_leave.available_days += leave_request.approved_available_days
     available_leave.carryforward_days += leave_request.approved_carryforward_days
```

## S14 `horilla_api.api_views.leave.views.xǁLeaveRequestRejectAPIViewǁleave_calculation__mutmut_6`

Function: `LeaveRequestRejectAPIView.leave_calculation`. Operator: built-in: 'employee_id=employee_id\n    '->''

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -1,8 +1,7 @@
 def leave_calculation(self, leave_request, employee_id):
     leave_type_id = leave_request.leave_type_id
     available_leave = AvailableLeave.objects.get(
-        leave_type_id=leave_type_id, employee_id=employee_id
-    )
+        leave_type_id=leave_type_id, )
     available_leave.available_days += leave_request.approved_available_days
     available_leave.carryforward_days += leave_request.approved_carryforward_days
     available_leave.save()
```

## S15 `horilla_api.api_views.leave.views.xǁLeaveRequestRejectAPIViewǁleave_calculation__mutmut_9`

Function: `LeaveRequestRejectAPIView.leave_calculation`. Operator: built-in: '+'->''

```diff
--- horilla_api/api_views/leave/views.py
+++ horilla_api/api_views/leave/views.py
@@ -4,7 +4,7 @@
         leave_type_id=leave_type_id, employee_id=employee_id
     )
     available_leave.available_days += leave_request.approved_available_days
-    available_leave.carryforward_days += leave_request.approved_carryforward_days
+    available_leave.carryforward_days = leave_request.approved_carryforward_days
     available_leave.save()
     leave_request.approved_available_days = 0
     leave_request.approved_carryforward_days = 0
```

## S16 `leave.models.x_cal_effective_requested_days__mutmut_12`

Function: `cal_effective_requested_days`. Operator: built-in: 'empl'->'N' | 'ye'->'n'

```diff
--- leave/models.py
+++ leave/models.py
@@ -9,7 +9,7 @@
     holiday_qs = Holidays.objects.all()
     if employee:
         holiday_qs = Holidays.objects.filter(
-            Q(is_specific=False) | Q(employees=employee)
+            Q(is_specific=False) | Q(employees=None)
         )
     holidays = set(holiday_dates_list(holiday_qs))
     company_leave_dates = set(
```

## S17 `leave.models.x_cal_effective_requested_days__mutmut_20`

Function: `cal_effective_requested_days`. Operator: built-in: 'e'->'No' | 'd_dat'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -13,7 +13,7 @@
         )
     holidays = set(holiday_dates_list(holiday_qs))
     company_leave_dates = set(
-        company_leave_dates_list(CompanyLeaves.objects.all(), start_date, end_date)
+        company_leave_dates_list(CompanyLeaves.objects.all(), start_date, None)
     )
 
     if (
```

## S18 `leave.models.x_cal_effective_requested_days__mutmut_22`

Function: `cal_effective_requested_days`. Operator: built-in: 'start_date, '->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -13,7 +13,7 @@
         )
     holidays = set(holiday_dates_list(holiday_qs))
     company_leave_dates = set(
-        company_leave_dates_list(CompanyLeaves.objects.all(), start_date, end_date)
+        company_leave_dates_list(CompanyLeaves.objects.all(), end_date)
     )
 
     if (
```

## S19 `leave.models.x_cal_effective_requested_days__mutmut_23`

Function: `cal_effective_requested_days`. Operator: built-in: 'end_date'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -13,7 +13,7 @@
         )
     holidays = set(holiday_dates_list(holiday_qs))
     company_leave_dates = set(
-        company_leave_dates_list(CompanyLeaves.objects.all(), start_date, end_date)
+        company_leave_dates_list(CompanyLeaves.objects.all(), start_date, )
     )
 
     if (
```

## S20 `leave.models.xǁLeaveAllocationRequestǁclean__mutmut_7`

Function: `LeaveAllocationRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -2,6 +2,6 @@
     if self.status != "requested":
         raise ValidationError(
             _(
-                "This form cannot be edited because the status is Requested / Rejected."
+                "XXThis form cannot be edited because the status is Requested / Rejected.XX"
             )
         )
```

## S21 `leave.models.xǁLeaveAllocationRequestǁclean__mutmut_8`

Function: `LeaveAllocationRequest.clean`. Operator: built-in: 'T'->'t' | 'R'->'r' | 'R'->'r'

```diff
--- leave/models.py
+++ leave/models.py
@@ -2,6 +2,6 @@
     if self.status != "requested":
         raise ValidationError(
             _(
-                "This form cannot be edited because the status is Requested / Rejected."
+                "this form cannot be edited because the status is requested / rejected."
             )
         )
```

## S22 `leave.models.xǁLeaveRequestǁclean__mutmut_1`

Function: `LeaveRequest.clean`. Operator: built-in: 'sup'->'Non' | 'r().clean()'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -1,5 +1,5 @@
 def clean(self):
-    cleaned_data = super().clean()
+    cleaned_data = None
     leave_type = getattr(self, "leave_type_id", None)
     if not leave_type:  # 836
         return
```

## S23 `leave.models.xǁLeaveRequestǁclean__mutmut_16`

Function: `LeaveRequest.clean`. Operator: built-in: 'None'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -3,7 +3,7 @@
     leave_type = getattr(self, "leave_type_id", None)
     if not leave_type:  # 836
         return
-    attachment = getattr(self, "attachment", None)
+    attachment = getattr(self, "attachment", )
     requ_days = set(self.requested_dates())
     restricted_leaves = RestrictLeave.objects.all()
     request = getattr(horilla_middlewares._thread_locals, "request", None)
```

## S24 `leave.models.xǁLeaveRequestǁclean__mutmut_27`

Function: `LeaveRequest.clean`. Operator: built-in: 'None'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -6,7 +6,7 @@
     attachment = getattr(self, "attachment", None)
     requ_days = set(self.requested_dates())
     restricted_leaves = RestrictLeave.objects.all()
-    request = getattr(horilla_middlewares._thread_locals, "request", None)
+    request = getattr(horilla_middlewares._thread_locals, "request", )
 
     # Check if leave type is assigned to employee
     if not AvailableLeave.objects.filter(
```

## S25 `leave.models.xǁLeaveRequestǁclean__mutmut_33`

Function: `LeaveRequest.clean`. Operator: built-in: ' employee_id=self.employee_id,'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -10,7 +10,7 @@
 
     # Check if leave type is assigned to employee
     if not AvailableLeave.objects.filter(
-        employee_id=self.employee_id, leave_type_id=leave_type
+        leave_type_id=leave_type
     ).exists():
         raise ValidationError(
             {
```

## S26 `leave.models.xǁLeaveRequestǁclean__mutmut_34`

Function: `LeaveRequest.clean`. Operator: built-in: 'leave_type_id=leave_type\n    '->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -10,8 +10,7 @@
 
     # Check if leave type is assigned to employee
     if not AvailableLeave.objects.filter(
-        employee_id=self.employee_id, leave_type_id=leave_type
-    ).exists():
+        employee_id=self.employee_id, ).exists():
         raise ValidationError(
             {
                 "leave_type_id": _(
```

## S27 `leave.models.xǁLeaveRequestǁclean__mutmut_36`

Function: `LeaveRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -14,7 +14,7 @@
     ).exists():
         raise ValidationError(
             {
-                "leave_type_id": _(
+                "XXleave_type_idXX": _(
                     "The selected leave type is not assigned to this employee."
                 )
             }
```

## S28 `leave.models.xǁLeaveRequestǁclean__mutmut_37`

Function: `LeaveRequest.clean`. Operator: built-in: 'leave'->'LEAVE' | 'type'->'TYPE' | 'id'->'ID'

```diff
--- leave/models.py
+++ leave/models.py
@@ -14,7 +14,7 @@
     ).exists():
         raise ValidationError(
             {
-                "leave_type_id": _(
+                "LEAVE_TYPE_ID": _(
                     "The selected leave type is not assigned to this employee."
                 )
             }
```

## S29 `leave.models.xǁLeaveRequestǁclean__mutmut_39`

Function: `LeaveRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -15,7 +15,7 @@
         raise ValidationError(
             {
                 "leave_type_id": _(
-                    "The selected leave type is not assigned to this employee."
+                    "XXThe selected leave type is not assigned to this employee.XX"
                 )
             }
         )
```

## S30 `leave.models.xǁLeaveRequestǁclean__mutmut_40`

Function: `LeaveRequest.clean`. Operator: built-in: 'T'->'t'

```diff
--- leave/models.py
+++ leave/models.py
@@ -15,7 +15,7 @@
         raise ValidationError(
             {
                 "leave_type_id": _(
-                    "The selected leave type is not assigned to this employee."
+                    "the selected leave type is not assigned to this employee."
                 )
             }
         )
```

## S31 `leave.models.xǁLeaveRequestǁclean__mutmut_45`

Function: `LeaveRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -22,7 +22,7 @@
 
     # Date validations
     if self.start_date > self.end_date:
-        raise ValidationError(_("End date should not be less than start date."))
+        raise ValidationError(_("XXEnd date should not be less than start date.XX"))
 
     if (
         self.start_date == self.end_date
```

## S32 `leave.models.xǁLeaveRequestǁclean__mutmut_53`

Function: `LeaveRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -29,7 +29,7 @@
         and self.start_date_breakdown != self.end_date_breakdown
     ):
         raise ValidationError(
-            _("Mismatch in the breakdown of the start and end date.")
+            _("XXMismatch in the breakdown of the start and end date.XX")
         )
 
     # Attachment requirement
```

## S33 `leave.models.xǁLeaveRequestǁclean__mutmut_63`

Function: `LeaveRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -35,7 +35,7 @@
     # Attachment requirement
     if leave_type and leave_type.require_attachment == "yes" and not attachment:
         raise ValidationError(
-            {"attachment": _("An attachment is required for this leave request")}
+            {"XXattachmentXX": _("An attachment is required for this leave request")}
         )
 
     # Overlapping leave check
```

## S34 `leave.models.xǁLeaveRequestǁclean__mutmut_64`

Function: `LeaveRequest.clean`. Operator: built-in: 'attachment'->'ATTACHMENT'

```diff
--- leave/models.py
+++ leave/models.py
@@ -35,7 +35,7 @@
     # Attachment requirement
     if leave_type and leave_type.require_attachment == "yes" and not attachment:
         raise ValidationError(
-            {"attachment": _("An attachment is required for this leave request")}
+            {"ATTACHMENT": _("An attachment is required for this leave request")}
         )
 
     # Overlapping leave check
```

## S35 `leave.models.xǁLeaveRequestǁclean__mutmut_66`

Function: `LeaveRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -35,7 +35,7 @@
     # Attachment requirement
     if leave_type and leave_type.require_attachment == "yes" and not attachment:
         raise ValidationError(
-            {"attachment": _("An attachment is required for this leave request")}
+            {"attachment": _("XXAn attachment is required for this leave requestXX")}
         )
 
     # Overlapping leave check
```

## S36 `leave.models.xǁLeaveRequestǁclean__mutmut_67`

Function: `LeaveRequest.clean`. Operator: built-in: 'A'->'a'

```diff
--- leave/models.py
+++ leave/models.py
@@ -35,7 +35,7 @@
     # Attachment requirement
     if leave_type and leave_type.require_attachment == "yes" and not attachment:
         raise ValidationError(
-            {"attachment": _("An attachment is required for this leave request")}
+            {"attachment": _("an attachment is required for this leave request")}
         )
 
     # Overlapping leave check
```

## S37 `leave.models.xǁLeaveRequestǁclean__mutmut_69`

Function: `LeaveRequest.clean`. Operator: built-in: 'and'->'or'

```diff
--- leave/models.py
+++ leave/models.py
@@ -39,7 +39,7 @@
         )
 
     # Overlapping leave check
-    if self.start_date and self.end_date:
+    if self.start_date or self.end_date:
         overlapping_requests = self.leaveoverlapping().exclude(id=self.id)
         if overlapping_requests.exclude(
             status__in=["cancelled", "rejected"]
```

## S38 `leave.models.xǁLeaveRequestǁclean__mutmut_71`

Function: `LeaveRequest.clean`. Operator: built-in: 's'->'Non' | 'lf.id'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -40,7 +40,7 @@
 
     # Overlapping leave check
     if self.start_date and self.end_date:
-        overlapping_requests = self.leaveoverlapping().exclude(id=self.id)
+        overlapping_requests = self.leaveoverlapping().exclude(id=None)
         if overlapping_requests.exclude(
             status__in=["cancelled", "rejected"]
         ).exists():
```

## S39 `leave.models.xǁLeaveRequestǁclean__mutmut_81`

Function: `LeaveRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -45,7 +45,7 @@
             status__in=["cancelled", "rejected"]
         ).exists():
             raise ValidationError(
-                _("Employee already has a leave request for this date range.")
+                _("XXEmployee already has a leave request for this date range.XX")
             )
 
     # Past date restriction
```

## S40 `leave.models.xǁLeaveRequestǁclean__mutmut_82`

Function: `LeaveRequest.clean`. Operator: built-in: 'E'->'e'

```diff
--- leave/models.py
+++ leave/models.py
@@ -45,7 +45,7 @@
             status__in=["cancelled", "rejected"]
         ).exists():
             raise ValidationError(
-                _("Employee already has a leave request for this date range.")
+                _("employee already has a leave request for this date range.")
             )
 
     # Past date restriction
```

## S41 `leave.models.xǁLeaveRequestǁclean__mutmut_103`

Function: `LeaveRequest.clean`. Operator: built-in: ' enabled=True,'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -56,7 +56,7 @@
             None,
         )
         restrict = EmployeePastLeaveRestrict.objects.filter(
-            enabled=True, company_id=emp_company
+            company_id=emp_company
         ).first()
         if restrict and self.start_date < date.today():
             raise ValidationError(_("Requests cannot be made for past dates."))
```

## S42 `leave.models.xǁLeaveRequestǁclean__mutmut_104`

Function: `LeaveRequest.clean`. Operator: built-in: 'company_id=emp_company\n        '->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -56,8 +56,7 @@
             None,
         )
         restrict = EmployeePastLeaveRestrict.objects.filter(
-            enabled=True, company_id=emp_company
-        ).first()
+            enabled=True, ).first()
         if restrict and self.start_date < date.today():
             raise ValidationError(_("Requests cannot be made for past dates."))
 
```

## S43 `leave.models.xǁLeaveRequestǁclean__mutmut_110`

Function: `LeaveRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -59,7 +59,7 @@
             enabled=True, company_id=emp_company
         ).first()
         if restrict and self.start_date < date.today():
-            raise ValidationError(_("Requests cannot be made for past dates."))
+            raise ValidationError(_("XXRequests cannot be made for past dates.XX"))
 
     # Avaialable leave days and requested leave days checking
     available_leave = AvailableLeave.objects.get(
```

## S44 `leave.models.xǁLeaveRequestǁclean__mutmut_111`

Function: `LeaveRequest.clean`. Operator: built-in: 'R'->'r'

```diff
--- leave/models.py
+++ leave/models.py
@@ -59,7 +59,7 @@
             enabled=True, company_id=emp_company
         ).first()
         if restrict and self.start_date < date.today():
-            raise ValidationError(_("Requests cannot be made for past dates."))
+            raise ValidationError(_("requests cannot be made for past dates."))
 
     # Avaialable leave days and requested leave days checking
     available_leave = AvailableLeave.objects.get(
```

## S45 `leave.models.xǁLeaveRequestǁclean__mutmut_116`

Function: `LeaveRequest.clean`. Operator: built-in: ' employee_id=self.employee_id,'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -63,7 +63,7 @@
 
     # Avaialable leave days and requested leave days checking
     available_leave = AvailableLeave.objects.get(
-        employee_id=self.employee_id, leave_type_id=leave_type
+        leave_type_id=leave_type
     )
 
     requested_days = calculate_requested_days(
```

## S46 `leave.models.xǁLeaveRequestǁclean__mutmut_117`

Function: `LeaveRequest.clean`. Operator: built-in: 'leave_type_id=leave_type\n    '->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -63,8 +63,7 @@
 
     # Avaialable leave days and requested leave days checking
     available_leave = AvailableLeave.objects.get(
-        employee_id=self.employee_id, leave_type_id=leave_type
-    )
+        employee_id=self.employee_id, )
 
     requested_days = calculate_requested_days(
         self.start_date,
```

## S47 `leave.models.xǁLeaveRequestǁclean__mutmut_122`

Function: `LeaveRequest.clean`. Operator: built-in: 's'->'Non' | 'lf.end_date_breakdown'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -70,7 +70,7 @@
         self.start_date,
         self.end_date,
         self.start_date_breakdown,
-        self.end_date_breakdown,
+        None,
     )
     effective_requested_days = cal_effective_requested_days(
         start_date=self.start_date,
```

## S48 `leave.models.xǁLeaveRequestǁclean__mutmut_129`

Function: `LeaveRequest.clean`. Operator: built-in: 'self.e'->'No' | 'd_dat'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -74,7 +74,7 @@
     )
     effective_requested_days = cal_effective_requested_days(
         start_date=self.start_date,
-        end_date=self.end_date,
+        end_date=None,
         leave_type_id=leave_type,
         requested_days=requested_days,
         employee=self.employee_id,
```

## S49 `leave.models.xǁLeaveRequestǁclean__mutmut_132`

Function: `LeaveRequest.clean`. Operator: built-in: 's'->'Non' | 'lf.employee_id'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -77,7 +77,7 @@
         end_date=self.end_date,
         leave_type_id=leave_type,
         requested_days=requested_days,
-        employee=self.employee_id,
+        employee=None,
     )
 
     if effective_requested_days <= 0:
```

## S50 `leave.models.xǁLeaveRequestǁclean__mutmut_137`

Function: `LeaveRequest.clean`. Operator: built-in: 'employee=self.employee_id,\n    '->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -77,8 +77,7 @@
         end_date=self.end_date,
         leave_type_id=leave_type,
         requested_days=requested_days,
-        employee=self.employee_id,
-    )
+        )
 
     if effective_requested_days <= 0:
         raise ValidationError(
```

## S51 `leave.models.xǁLeaveRequestǁclean__mutmut_142`

Function: `LeaveRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -83,7 +83,7 @@
     if effective_requested_days <= 0:
         raise ValidationError(
             _(
-                "The requested days for this leave type is zero. Please check the "
+                "XXThe requested days for this leave type is zero. Please check the XX"
                 "selected dates, breakdown and the leave type's holiday/company "
                 "leave exclusion settings."
             )
```

## S52 `leave.models.xǁLeaveRequestǁclean__mutmut_143`

Function: `LeaveRequest.clean`. Operator: built-in: 'T'->'t' | 'P'->'p'

```diff
--- leave/models.py
+++ leave/models.py
@@ -83,7 +83,7 @@
     if effective_requested_days <= 0:
         raise ValidationError(
             _(
-                "The requested days for this leave type is zero. Please check the "
+                "the requested days for this leave type is zero. please check the "
                 "selected dates, breakdown and the leave type's holiday/company "
                 "leave exclusion settings."
             )
```

## S53 `leave.models.xǁLeaveRequestǁclean__mutmut_147`

Function: `LeaveRequest.clean`. Operator: built-in: 'self.e'->'No' | 'd_dat'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -89,7 +89,7 @@
             )
         )
 
-    leave_dates = leave_requested_dates(self.start_date, self.end_date)
+    leave_dates = leave_requested_dates(self.start_date, None)
     month_year = [f"{date.year}-{date.strftime('%m')}" for date in leave_dates]
     today = datetime.today()
     unique_dates = list(set(month_year))
```

## S54 `leave.models.xǁLeaveRequestǁclean__mutmut_152`

Function: `LeaveRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -90,7 +90,7 @@
         )
 
     leave_dates = leave_requested_dates(self.start_date, self.end_date)
-    month_year = [f"{date.year}-{date.strftime('%m')}" for date in leave_dates]
+    month_year = [f"{date.year}-{date.strftime('XX%mXX')}" for date in leave_dates]
     today = datetime.today()
     unique_dates = list(set(month_year))
     if f"{today.month}-{today.year}" in unique_dates:
```

## S55 `leave.models.xǁLeaveRequestǁclean__mutmut_153`

Function: `LeaveRequest.clean`. Operator: built-in: 'm'->'M'

```diff
--- leave/models.py
+++ leave/models.py
@@ -90,7 +90,7 @@
         )
 
     leave_dates = leave_requested_dates(self.start_date, self.end_date)
-    month_year = [f"{date.year}-{date.strftime('%m')}" for date in leave_dates]
+    month_year = [f"{date.year}-{date.strftime('%M')}" for date in leave_dates]
     today = datetime.today()
     unique_dates = list(set(month_year))
     if f"{today.month}-{today.year}" in unique_dates:
```

## S56 `leave.models.xǁLeaveRequestǁclean__mutmut_160`

Function: `LeaveRequest.clean`. Operator: built-in: 'self.start_dat'->'Non'

```diff
--- leave/models.py
+++ leave/models.py
@@ -96,7 +96,7 @@
     if f"{today.month}-{today.year}" in unique_dates:
         unique_dates.remove(f"{today.strftime('%m')}-{today.year}")
 
-    forcated_days = available_leave.forcasted_leaves(self.start_date)
+    forcated_days = available_leave.forcasted_leaves(None)
 
     available_days = available_leave.available_days or 0
     carryforward_days = available_leave.carryforward_days or 0
```

## S57 `leave.models.xǁLeaveRequestǁclean__mutmut_163`

Function: `LeaveRequest.clean`. Operator: built-in: '0'->'1'

```diff
--- leave/models.py
+++ leave/models.py
@@ -98,7 +98,7 @@
 
     forcated_days = available_leave.forcasted_leaves(self.start_date)
 
-    available_days = available_leave.available_days or 0
+    available_days = available_leave.available_days or 1
     carryforward_days = available_leave.carryforward_days or 0
     carryforward_max = available_leave.leave_type_id.carryforward_max or 0
     carryforward_type = available_leave.leave_type_id.carryforward_type
```

## S58 `leave.models.xǁLeaveRequestǁclean__mutmut_166`

Function: `LeaveRequest.clean`. Operator: built-in: '0'->'1'

```diff
--- leave/models.py
+++ leave/models.py
@@ -99,7 +99,7 @@
     forcated_days = available_leave.forcasted_leaves(self.start_date)
 
     available_days = available_leave.available_days or 0
-    carryforward_days = available_leave.carryforward_days or 0
+    carryforward_days = available_leave.carryforward_days or 1
     carryforward_max = available_leave.leave_type_id.carryforward_max or 0
     carryforward_type = available_leave.leave_type_id.carryforward_type
 
```

## S59 `leave.models.xǁLeaveRequestǁclean__mutmut_169`

Function: `LeaveRequest.clean`. Operator: built-in: '0'->'1'

```diff
--- leave/models.py
+++ leave/models.py
@@ -100,7 +100,7 @@
 
     available_days = available_leave.available_days or 0
     carryforward_days = available_leave.carryforward_days or 0
-    carryforward_max = available_leave.leave_type_id.carryforward_max or 0
+    carryforward_max = available_leave.leave_type_id.carryforward_max or 1
     carryforward_type = available_leave.leave_type_id.carryforward_type
 
     if carryforward_type in ["carryforward", "carryforward expire"]:
```

## S60 `leave.models.xǁLeaveRequestǁclean__mutmut_187`

Function: `LeaveRequest.clean`. Operator: built-in: '+'->'-'

```diff
--- leave/models.py
+++ leave/models.py
@@ -108,7 +108,7 @@
     elif carryforward_type == "no carryforward":
         carryforward_days = 0
 
-    total_leave_days = available_days + carryforward_days + forcated_days
+    total_leave_days = available_days + carryforward_days - forcated_days
 
     if not effective_requested_days <= total_leave_days:
         raise ValidationError(
```

## S61 `leave.models.xǁLeaveRequestǁclean__mutmut_188`

Function: `LeaveRequest.clean`. Operator: custom:balance_term_drop (BR-01)

```diff
--- leave/models.py
+++ leave/models.py
@@ -108,7 +108,7 @@
     elif carryforward_type == "no carryforward":
         carryforward_days = 0
 
-    total_leave_days = available_days + carryforward_days + forcated_days
+    total_leave_days = (available_days + carryforward_days)
 
     if not effective_requested_days <= total_leave_days:
         raise ValidationError(
```

## S62 `leave.models.xǁLeaveRequestǁclean__mutmut_197`

Function: `LeaveRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -112,7 +112,7 @@
 
     if not effective_requested_days <= total_leave_days:
         raise ValidationError(
-            _("Does not have sufficient leave balance for the requested dates.")
+            _("XXDoes not have sufficient leave balance for the requested dates.XX")
         )
 
     # Get employee department and job if available
```

## S63 `leave.models.xǁLeaveRequestǁclean__mutmut_198`

Function: `LeaveRequest.clean`. Operator: built-in: 'D'->'d'

```diff
--- leave/models.py
+++ leave/models.py
@@ -112,7 +112,7 @@
 
     if not effective_requested_days <= total_leave_days:
         raise ValidationError(
-            _("Does not have sufficient leave balance for the requested dates.")
+            _("does not have sufficient leave balance for the requested dates.")
         )
 
     # Get employee department and job if available
```

## S64 `leave.models.xǁLeaveRequestǁclean__mutmut_212`

Function: `LeaveRequest.clean`. Operator: built-in: 'Fals'->'Non'

```diff
--- leave/models.py
+++ leave/models.py
@@ -131,7 +131,7 @@
         exclued_types = set(restrict.exclued_leave_types.all())
         specific_types = set(restrict.spesific_leave_types.all())
 
-        is_restricted = False
+        is_restricted = None
 
         # Determine if the current leave type is restricted
         if restrict.include_all and not exclued_types:
```

## S65 `leave.models.xǁLeaveRequestǁclean__mutmut_226`

Function: `LeaveRequest.clean`. Operator: built-in: 'continu'->'br' | ''->'ak'

```diff
--- leave/models.py
+++ leave/models.py
@@ -142,7 +142,7 @@
             is_restricted = True
 
         if not is_restricted:
-            continue
+            break
 
         restri_days = set(restrict_leaves(restrict.id))
         if not restri_days:
```

## S66 `leave.models.xǁLeaveRequestǁclean__mutmut_231`

Function: `LeaveRequest.clean`. Operator: built-in: 'continu'->'br' | ''->'ak'

```diff
--- leave/models.py
+++ leave/models.py
@@ -146,7 +146,7 @@
 
         restri_days = set(restrict_leaves(restrict.id))
         if not restri_days:
-            continue
+            break
 
         # Check if requested days intersect with restricted days
         if requ_days & restri_days:
```

## S67 `leave.models.xǁLeaveRequestǁclean__mutmut_241`

Function: `LeaveRequest.clean`. Operator: built-in: ''->'XX' | ''->'XX'

```diff
--- leave/models.py
+++ leave/models.py
@@ -157,7 +157,7 @@
             ) or (emp_job and emp_job in restrict.job_position.all()):
                 raise ValidationError(
                     _(
-                        "You cannot request leave for this date range. The requested dates are restricted. Please contact admin."
+                        "XXYou cannot request leave for this date range. The requested dates are restricted. Please contact admin.XX"
                     )
                 )
 
```

## S68 `leave.models.xǁLeaveRequestǁclean__mutmut_242`

Function: `LeaveRequest.clean`. Operator: built-in: 'Y'->'y' | 'T'->'t' | 'P'->'p'

```diff
--- leave/models.py
+++ leave/models.py
@@ -157,7 +157,7 @@
             ) or (emp_job and emp_job in restrict.job_position.all()):
                 raise ValidationError(
                     _(
-                        "You cannot request leave for this date range. The requested dates are restricted. Please contact admin."
+                        "you cannot request leave for this date range. the requested dates are restricted. please contact admin."
                     )
                 )
 
```

## S69 `leave.models.xǁLeaveRequestǁleaveoverlapping__mutmut_2`

Function: `LeaveRequest.leaveoverlapping`. Operator: built-in: 's'->'Non' | 'lf.id'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -6,7 +6,7 @@
         employee_id=self.employee_id,
         start_date__lte=self.end_date,
         end_date__gte=self.start_date,
-    ).exclude(id=self.id)
+    ).exclude(id=None)
 
     if overlapping_requests.exists():
         existing_leave = overlapping_requests.first()
```

## S70 `leave.models.xǁLeaveRequestǁleaveoverlapping__mutmut_6`

Function: `LeaveRequest.leaveoverlapping`. Operator: built-in: '        employee_id=self.employee_id,'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -3,7 +3,6 @@
         Checks for overlapping leave requests based on the current instance's dates and employee.
         """
     overlapping_requests = LeaveRequest.objects.filter(
-        employee_id=self.employee_id,
         start_date__lte=self.end_date,
         end_date__gte=self.start_date,
     ).exclude(id=self.id)
```

## S71 `leave.models.xǁLeaveRequestǁleaveoverlapping__mutmut_7`

Function: `LeaveRequest.leaveoverlapping`. Operator: built-in: '        start_date__lte=self.end_date,'->''

```diff
--- leave/models.py
+++ leave/models.py
@@ -4,7 +4,6 @@
         """
     overlapping_requests = LeaveRequest.objects.filter(
         employee_id=self.employee_id,
-        start_date__lte=self.end_date,
         end_date__gte=self.start_date,
     ).exclude(id=self.id)
 
```

