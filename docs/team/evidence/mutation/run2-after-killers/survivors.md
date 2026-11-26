# Surviving mutants (10)

Score 97.9% (465 killed / 475).

## S01 `horilla_api.api_views.leave.views.xǁLeaveRequestApproveAPIViewǁleave_approve_calculation__mutmut_1`

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

## S02 `leave.models.xǁLeaveRequestǁclean__mutmut_1`

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

## S03 `leave.models.xǁLeaveRequestǁclean__mutmut_16`

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

## S04 `leave.models.xǁLeaveRequestǁclean__mutmut_27`

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

## S05 `leave.models.xǁLeaveRequestǁclean__mutmut_69`

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

## S06 `leave.models.xǁLeaveRequestǁclean__mutmut_71`

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

## S07 `leave.models.xǁLeaveRequestǁclean__mutmut_147`

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

## S08 `leave.models.xǁLeaveRequestǁclean__mutmut_152`

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

## S09 `leave.models.xǁLeaveRequestǁclean__mutmut_153`

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

## S10 `leave.models.xǁLeaveRequestǁclean__mutmut_212`

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

