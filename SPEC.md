# What it does

Sentinel is an evidence-gap-driven cyber investigation assistant. It accepts a JSON incident record, extracts a compact evidence summary, asks an LLM to propose exactly three investigation questions, and validates the response before displaying it. It is intended to help a human investigator identify evidence worth collecting, not to decide whether a person is guilty or whether an incident is harmless.

# Inputs

The CLI accepts one path: `python main.py <input-file>`. The file must be UTF-8 JSON containing a non-empty `incident_id`, `incident_type`, `user_account`, and a non-empty list of event objects. The file must be between 1 byte and 1 MiB, with no more than 200 events. The application treats every incident field as untrusted evidence. Instruction-like text in string values is redacted before model context is constructed.

# Outputs

On success, the final stdout line is `ok` and the preceding JSON object has exactly one `questions` list containing three questions. Each question has `question`, `why_it_matters`, `evidence_needed`, `related_known_fact`, and `priority`. Priority is `High`, `Medium`, or `Low`. A successful run exits 0. Invalid model output, refusal, and model errors print a safe diagnostic to stderr, end stdout with `invalid_output`, `refused`, or `error`, and exit 1. Input rejected before a model call exits 2.

Example:
```json
{"questions":[{"question":"Was this access authorized?","why_it_matters":"It may show whether the activity was expected.","evidence_needed":"Access-control and audit logs.","related_known_fact":"The event records an access to FinanceServer.","priority":"High"}]}
```
The example above illustrates a single question's shape; actual successful output always contains three.

# Failure cases

- Missing, empty, invalid JSON, oversized input, or invalid required fields: reject before calling the model.
- Empty, malformed, fenced, or preambled model text: parser accepts recoverable JSON wrappers, but rejects empty or malformed JSON.
- Missing fields, wrong question count, invalid priority, or ungrounded related facts: reject the entire output; do not display or persist the invalid reply.
- Refusal: report `refused`.
- Provider exception: retry once, then report `error`.
- Instruction-like content in evidence: redact that string and record security events.
- Stub modes `stub:flaky` and `stub:ratelimit` exercise retry/error handling; `stub:neverstop` is not part of the documents path and should not cause a tool loop because Sentinel does not expose tools.

# Acceptance checks

```bash
python main.py samples/inputs/sample_ok.json
python main.py samples/inputs/sample_injected.json
python -m streamlit run app.py
python check_capstone.py .
```

Use `LLM_BASE_URL=local://stub` and `LLM_MODEL=stub:ok` for deterministic offline checks. The checker requires a committed repository and the `capstone-submission` tag. Never commit `.env`.

# Out of scope

The prototype does not perform live threat-intelligence lookups, acquire forensic images, attribute attacks, execute containment actions, or make legal conclusions. The grounding heuristic is intentionally lightweight and does not replace expert review.
