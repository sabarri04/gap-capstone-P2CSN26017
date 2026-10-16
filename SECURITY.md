# What this application is

Sentinel turns incident JSON into prioritized questions about evidence that a cybersecurity investigator may need to collect. It is a decision-support prototype. It must not be treated as an autonomous incident verdict or a replacement for forensic procedures.

# Trust boundaries

Incident JSON is untrusted, including fields named `details`, `resource`, and any other string. Model responses are also untrusted until parsed and validated. The model provider receives only the sanitized incident summary and prompt. API credentials are read from environment variables and must not be committed. Operational records are written to `run_log.jsonl` and `security_log.jsonl`; neither log should contain the full prompt, full response, or API key.

# What an attacker could try

- Prompt injection inside an event's details, such as a request to change the model's task.
- Malformed or oversized JSON to consume resources or crash the parser.
- A model reply with invalid JSON, missing fields, too few questions, or an invalid priority.
- A fabricated `related_known_fact` that is not supported by the incident.
- A model refusal or provider error that might be accidentally shown as a successful result.
- HTML-like strings in incident data or model output intended to affect the UI.

# The guardrails in place

| Guardrail | File and function | Which attack it addresses |
|---|---|---|
| Input size, type and schema checks | `pipeline.py:load_incident` | Empty, malformed, oversized and structurally invalid input |
| Instruction-pattern redaction | `pipeline.py:_sanitize` | Common prompt-injection phrasings embedded in evidence |
| Security event audit | `security.py:log_event`, called by `pipeline.py:_sanitize` | Makes guardrail invocation observable |
| Pydantic output schema | `pipeline.py:InvestigationOutput` and `InvestigationQuestion` | Missing fields, wrong question count, empty text, invalid priority |
| Evidence-overlap check | `pipeline.py:_grounded` | Some fabricated related facts |
| Status-only failure reporting | `main.py:main`, `pipeline.py:run_pipeline` | Prevents invalid model replies being printed as success |
| Model-call logging | `observability.py:log_call` | Makes latency, status, token estimates and cost auditable |

# What each guardrail does not stop

- Pattern redaction does not recognize every possible indirect or multilingual injection.
- Pydantic checks shape and field constraints, not whether every claim is true.
- The evidence-overlap check is a simple lexical heuristic; matching words can still be misleading.
- Local logs can expose operational metadata and should be access-controlled and rotated.
- UI escaping and browser protections are not a substitute for reviewing all future rendering changes.
- A provider may retain submitted content under its own terms; do not upload sensitive real incident data without authorization.

# What I would do with more time

- Use a broader injection classifier and adversarial test corpus, including multilingual and encoded payloads.
- Replace lexical grounding with evidence IDs and citations to individual events.
- Add HTML escaping for every untrusted value rendered in the UI and conduct a security review of the rendering layer.
- Add structured unit tests and measure false positives/false negatives on realistic incident examples.
- Add authentication, role-based access, log retention controls, and a privacy review before any operational deployment.
