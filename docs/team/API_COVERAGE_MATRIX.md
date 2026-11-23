# Area 2 API coverage matrix: current B checkpoint

Owner: Syed Muhammad Rayyan Hassan, **24I-3000**, 23 November 2026.

**Generation is verified; HTTP execution is blocked.** This is not the completed all-input/API coverage matrix required for final submission. The spec has 16 paths / 27 operations. Counts below come from generated output, not executed API cases.

Generated data: 518 cases (458 EP, 60 BVA); 66 operation/input entries. HTTP cases planned in B: 5; executed: 0.

| Operation | Method and route | Inputs inventoried | Generated EP | Generated BVA | HTTP status |
|---|---|---:|---:|---:|---|
| `allocation_approve` | `PUT /api/v1/leave/allocation-approve/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `allocation_reject` | `PUT /api/v1/leave/allocation-reject/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `allocation_list` | `GET /api/v1/leave/allocation-request/` | 0 | 0 | 0 | Not executed; broader coverage in C |
| `allocation_create` | `POST /api/v1/leave/allocation-request/` | 5 | 34 | 6 | Not executed; broader coverage in C |
| `allocation_delete` | `DELETE /api/v1/leave/allocation-request/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `allocation_detail` | `GET /api/v1/leave/allocation-request/{pk}/` | 1 | 7 | 0 | Readback used by slice, blocked |
| `allocation_update` | `PUT /api/v1/leave/allocation-request/{pk}/` | 6 | 41 | 6 | Not executed; broader coverage in C |
| `approve` | `PUT /api/v1/leave/approve/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `own_balance` | `GET /api/v1/leave/available-leave/` | 0 | 0 | 0 | Readback used by slice, blocked |
| `cancel` | `PUT /api/v1/leave/cancel/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `cancellation_approve` | `PUT /api/v1/leave/cancellation-approve/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `cancellation_reject` | `PUT /api/v1/leave/cancellation-reject/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `reject` | `PUT /api/v1/leave/reject/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `leave_list` | `GET /api/v1/leave/request/` | 0 | 0 | 0 | Not executed; broader coverage in C |
| `leave_create` | `POST /api/v1/leave/request/` | 8 | 56 | 9 | Not executed; broader coverage in C |
| `leave_delete` | `DELETE /api/v1/leave/request/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `leave_detail` | `GET /api/v1/leave/request/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `leave_update` | `PUT /api/v1/leave/request/{pk}/` | 9 | 63 | 9 | Not executed; broader coverage in C |
| `self_allocation_list` | `GET /api/v1/leave/user-allocation-request/` | 0 | 0 | 0 | Readback used by slice, blocked |
| `self_allocation_create` | `POST /api/v1/leave/user-allocation-request/` | 4 | 27 | 6 | 5 selected cases blocked |
| `self_allocation_delete` | `DELETE /api/v1/leave/user-allocation-request/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `self_allocation_update` | `PUT /api/v1/leave/user-allocation-request/{pk}/` | 5 | 34 | 6 | Not executed; broader coverage in C |
| `self_leave_list` | `GET /api/v1/leave/user-request/` | 0 | 0 | 0 | Not executed; broader coverage in C |
| `self_leave_create` | `POST /api/v1/leave/user-request/` | 7 | 49 | 9 | Not executed; broader coverage in C |
| `self_leave_delete` | `DELETE /api/v1/leave/user-request/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `self_leave_detail` | `GET /api/v1/leave/user-request/{pk}/` | 1 | 7 | 0 | Not executed; broader coverage in C |
| `self_leave_update` | `PUT /api/v1/leave/user-request/{pk}/` | 8 | 56 | 9 | Not executed; broader coverage in C |

## Input-category accounting

| Category | Generated support | Manually / dynamically bound | Remaining verification or justified N/A |
|---|---|---|---|
| Required/optional/null/body leaves | Explicit omission versus null, type, empty/nonblank/trimmed text, nested object leaves | Baselines use only synthetic values | Entire-body omission/null and framework-specific coercions are excluded. |
| Allocation numeric amount | Finite number; negative/zero/positive, missing/null/nonnumeric/type | Baseline amount comes from the spec example, never a hardcoded endpoint limit | No declared numeric min/max; numeric BVA N/A. Positive-only business policy not invented. |
| Breakdown enum | Every declared member and invalid choice | Full-day baseline avoids unrelated mismatch | Enum has no ordered bound; BVA N/A. Same-day matching combinations remain C. |
| Dates | Calendar format; relative end-date/start-date three-point boundary | Stable date anchor/end date in bindings | Balance, holiday, overlap and conditional breakdown constraints remain C. Absolute date bounds are supported by focused fixtures, not invented in production. |
| Attachment | Missing/null/type/empty content/name; 99/100/101 filename BVA | Synthetic in-memory ASCII descriptor serialized by Requests | Actual serializer-default introspection and HTTP pending; no file-byte limit fabricated. |
| IDs and path references | Integer/type/fraction/required and missing-record classes | Runtime employee/type IDs from unchanged seed | Other IDs remain symbolic in this slice; missing-record and owner/state cases require C setup. No numeric upper ID limit. |
| Collection/boolean/nested schema capabilities | Verified on small generator fixtures | Not added as artificial fields to production endpoints | They are generator capability checks, not executed workflow coverage. Item constraints are predicates; recursive item EP/BVA expansion is not claimed. |
| Filter/search/grouping/pagination | Explicitly excluded from this reconstructed contract | None | Must restore/review A inventory; page_size maximum is a clamp and not a rejection boundary. |
| Rejection reason | Explicitly excluded from body generation | None | Normalize/ignore/truncate behavior and persistence-limit conflict require C source/oracle review. |
| Balance/state/permissions/repetition | No complete generation or execution claim | Only normal roles and unchanged balance checked by the B slice once runnable | BR-01/BR-03/BR-04 and remaining BR-02 scenarios pending full A/C basis. |

## Requirement mapping and denominators

| Requirement | B contribution | Current acceptance |
|---|---|---|
| R3 / R4: EP and three-point BVA on every selected input | Source-derived schema classes, real filename and relative-date limits, explicit exclusions | Partial. Do not treat generated subset counts as every-input completion. |
| R5: API tests consume generator output | Canonical artifact freshness check; runtime-bound JSON generation/readback; five parametrized HTTP cases | Code present, real consumption execution blocked at missing pytest. |
| FR-01 / FR-10 | Allocation creation and unchanged balance readback slice | 0/5 intended B HTTP cases executed; no pass percentage claimed. |
| R12 / R16: management / truthful disclosure | Status, risk/activity, evidence and AI-use records | Updated locally; group management/viva and remote own-account contribution still pending. |

## Outstanding source exclusions

1. Phase A archive/report/runtime evidence unavailable locally; this is a source-reconstructed scoped contract, not the recovered or live-validated Phase A contract.
2. Filter/search/grouping/page/page_size query inputs and assign-leave administration remain unreviewed here; pagination is coercion/clamping, not a declared rejection maximum.
3. Optional reject reason is normalized/ignored/truncated by helper, not schema-validated; body generation for rejection and its persistence mismatch require Phase C oracle review.
4. Date ordering has generated relative calendar-day BVA. Other relational breakdown/overlap/attachment-required and effective balance/carry-forward/forecast rules require runtime scenario binding; isolated schema cases may violate those relations and are not automatically safe HTTP cases.
5. Path integer routing/existence and role/state transitions need Phase C expectations; positive/existing symbolic values are scenario placeholders, not proven database records.
6. DRF coercions (including numeric strings) and file-null/form omission are not exhaustively modeled; generated predicates concern declared schema classes, not guaranteed HTTP status.
7. Attachment 100-character filename bound derives from Django/DRF defaults; verify serializer introspection and HTTP before accepting this as runtime evidence.
8. Entire-body omission/null, binary byte/file-size limits and multipart collection encodings are outside this reader; body leaves and synthetic ASCII file descriptors are supported.

## Artifact lineage

- Spec canonical SHA-256: `0b090bc8a58c0d56e761c489ebb726b2bbc2d1b79feb1256d27981c1a965eb03`.
- Logical bindings SHA-256: `25b0b2a165dd1c31cf9ad9cdb0b317f1de106560b399cc9098e234a5875be4a0`.
- Generated data SHA-256: `16d79497f483aced4ecaac4f0741f6b870f0e93035dfe21feac3847c3915c64c`.

Regenerate this accounting after contract/data changes. `generated_cases.json` includes per-input source schema and BVA N/A entries; `AREA2_TEST_BASIS.md` explains source-backed assumptions. The complete two-real-constraint viva demonstration is reserved for D.
