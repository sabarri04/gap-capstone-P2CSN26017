# What this set covers

The deterministic capstone stub is used to exercise the pipeline and failure handling. The following are planned evaluation cases; results must be recorded after running the application against the real configured model. The sample inputs are synthetic and do not represent real people or systems.

# The rows

| # | Kind | Input | What must be true | Result |
|---|---|---|---|---|
| 1 | Ordinary | `samples/inputs/sample_ok.json` | Exactly three questions; fields and priorities valid; facts tied to incident events | Pending real-model run |
| 2 | Unusual but legitimate | A login from a new location with a successful MFA event | Questions investigate context without assuming compromise | Pending |
| 3 | Nothing wrong | Approved admin maintenance with a change ticket | Questions seek verification and avoid asserting maliciousness | Pending |
| 4 | Malformed or empty | Empty file / invalid JSON | Rejected before any model call | Covered by checker |
| 5 | Injected | `samples/inputs/sample_injected.json` | Injection-like details are redacted; no injected marker reaches output; guard event logged | Covered by checker |

# Metrics

| Metric | Value | Where it comes from |
|---|---|---|
| Accuracy | Pending: run evaluation rows against the configured real model | Human review against required facts |
| Speed | Populate after runs | `latency_ms` in `run_log.jsonl` |
| Cost | Estimate only when token counts are available; free-tier billed cost may be zero | `observability.py` token price constants and `run_log.jsonl` |

The price constants in `observability.py` are starter estimates, not a verified current quote for every provider. Verify the chosen model's pricing and document the source before reporting real costs. Estimated token counts are marked with `tokens_estimated=true`.

# Known failures

1. The injection filter uses known phrase patterns. An attacker can phrase an instruction differently or encode it, so the guardrail can miss it. The next improvement would be adversarial testing and layered classification.
2. Evidence grounding uses word overlap. A fabricated statement may contain a true identifier and pass the heuristic. The next improvement would be requiring each question to cite event IDs and checking those references.
3. Model responses can vary between runs, and the local stub cannot establish real-model accuracy. The next improvement would be to evaluate a fixed set of cases with a human-reviewed rubric.
4. This UI is a prototype and does not include user authentication or role-based access control. It should not be exposed publicly with sensitive data.

# What this set does not cover

The tests do not prove that the system detects every prompt injection, that every question is forensically sound, or that the application is safe for production. The synthetic data and deterministic stub only cover a limited set of input and response behaviours.
