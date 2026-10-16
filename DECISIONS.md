# Design decisions

1. **Documents path for item 6.** The project is an evidence-analysis workflow, so it treats incident JSON as an untrusted document and applies redaction plus audit events rather than inventing a tool-use feature unrelated to the current capstone.
2. **Pydantic response schema.** A strict typed schema makes question count, field constraints, and priority values explicit.
3. **Shared pipeline.** `main.py` and `app.py` both call `pipeline.run_pipeline`; this prevents CLI and UI behaviour from drifting.
4. **No raw failure reply.** Failed output is not printed or stored; stdout ends with a machine-readable status and details go to stderr or the UI's safe status message.
5. **Offline-first testing.** The supplied stub allows repeatable tests without API access. Real-model evaluation remains a separate human-reviewed task.
6. **No live enrichment.** Threat intelligence and active response actions are excluded to keep the prototype safe and scoped.
