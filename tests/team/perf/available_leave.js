// k6 load test: GET /api/leave/available-leave/ (the shared balance record read
// by both workflows). Limits were fixed before any run (RISK_REGISTER.md EC-3,
// PERFORMANCE_TESTING.md section 2): p95 <= 500 ms and < 1% unexpected failures.
//
// Usage (Horilla running on the seeded snapshot):
//   k6 run -e VUS=1 -e RUN=1vu-run1 tests/team/perf/available_leave.js
//   k6 run -e VUS=5 -e RUN=5vu-run1 tests/team/perf/available_leave.js
// Each run: 10 s warm-up at the target user count, then 60 s measured steady
// state. Only the steady-state requests count towards the limits.
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";

const BASE = __ENV.BASE_URL || "http://localhost:8000";
const VUS = Number(__ENV.VUS || 1);
const RUN = __ENV.RUN || `${VUS}vu`;
const OUT = __ENV.OUT || "docs/team/evidence/perf";
// Synthetic seed account (scripts/team/seed_team.py).
const USER = __ENV.PERF_USER || "team_employee";
const PASS = __ENV.PERF_PASS || "TeamEmploy#2026";
// Think time per user: one balance read per second, a realistic pace for a
// person in the leave screens, and it keeps 5 users (about 300 req/min) under
// Horilla's own per-user API throttle of 600 req/min.
const THINK_SECONDS = 1;

const unexpected = new Rate("unexpected_failures");

export const options = {
  scenarios: {
    warmup: { executor: "constant-vus", vus: VUS, duration: "10s", tags: { phase: "warmup" } },
    steady: { executor: "constant-vus", vus: VUS, duration: "60s", startTime: "10s", tags: { phase: "steady" } },
  },
  thresholds: {
    "http_req_duration{phase:steady}": ["p(95)<=500"],
    "unexpected_failures{phase:steady}": ["rate<0.01"],
    "http_req_failed{phase:steady}": ["rate<0.01"],
  },
  summaryTrendStats: ["avg", "min", "med", "p(90)", "p(95)", "max", "count"],
};

export function setup() {
  const res = http.post(`${BASE}/api/auth/login/`, JSON.stringify({ username: USER, password: PASS }), {
    headers: { "Content-Type": "application/json" },
    tags: { phase: "setup" },
  });
  if (res.status !== 200) throw new Error(`login failed: ${res.status}`);
  return { token: res.json("access") };
}

export default function (data) {
  const res = http.get(`${BASE}/api/leave/available-leave/`, {
    headers: { Authorization: `Bearer ${data.token}` },
  });
  const ok = check(res, {
    "status is 200": (r) => r.status === 200,
    "balance row present": (r) => r.status === 200 && Array.isArray(r.json("results")) && r.json("results").length > 0,
  });
  unexpected.add(!ok);
  sleep(THINK_SECONDS);
}

export function handleSummary(data) {
  const m = data.metrics;
  const steady = {
    run: RUN,
    vus: VUS,
    p95_ms: m["http_req_duration{phase:steady}"].values["p(95)"],
    p90_ms: m["http_req_duration{phase:steady}"].values["p(90)"],
    median_ms: m["http_req_duration{phase:steady}"].values.med,
    max_ms: m["http_req_duration{phase:steady}"].values.max,
    requests: m["http_req_duration{phase:steady}"].values.count,
    requests_per_second: m["http_req_duration{phase:steady}"].values.count / 60,
    unexpected_failure_rate: m["unexpected_failures{phase:steady}"].values.rate,
    thresholds_passed: Object.values(data.metrics)
      .filter((x) => x.thresholds)
      .every((x) => Object.values(x.thresholds).every((t) => t.ok)),
  };
  return {
    stdout: JSON.stringify(steady, null, 2) + "\n",
    [`${OUT}/k6-${RUN}-summary.json`]: JSON.stringify(data, null, 2),
    [`${OUT}/k6-${RUN}-steady.json`]: JSON.stringify(steady, null, 2),
  };
}
