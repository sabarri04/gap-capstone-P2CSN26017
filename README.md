# Sentinel — Evidence-Gap Driven Cyber Investigation Assistant

Sentinel analyzes a structured incident record and proposes three prioritized questions that help an investigator decide what evidence to collect next. It is a decision-support prototype, not an automated verdict system.

## Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Keep the default stub configuration in `.env` for offline testing. For a real OpenAI-compatible provider, set `LLM_API_KEY`, `LLM_BASE_URL`, and `LLM_MODEL`. Example Groq-compatible settings are shown in `.env.example`; confirm the model name and provider access before use.

## Run

```powershell
python main.py samples/inputs/sample_ok.json
python main.py samples/inputs/sample_injected.json
python -m streamlit run app.py
```

CLI statuses are the final stdout line. Success is `ok` (exit 0); model failures use `invalid_output`, `refused`, or `error` (exit 1); invalid input is rejected before a model call (exit 2).

## Test the stub

Set `LLM_MODEL` in `.env` to one of `stub:ok`, `stub:fenced`, `stub:preamble`, `stub:malformed`, `stub:badshape`, `stub:empty`, `stub:refused`, `stub:error`, `stub:flaky`, `stub:ratelimit`, `stub:obedient`, `stub:toolcall`, `stub:traversal`, `stub:neverstop`, or `stub:badargs`. Most modes are intended to test CLI behaviour; Sentinel uses the documents guardrail path and does not execute tools.

## Check

```powershell
python check_capstone.py .
```

The checker evaluates committed files. Commit your work, create the required tag `capstone-submission`, and then run the checker. Do not edit `client.py`, `stub_client.py`, or `check_capstone.py`.

## Logs and secrets

Model-call telemetry goes to `run_log.jsonl`; security guard events go to `security_log.jsonl`. Both are ignored by Git. `.env` must never be committed. If a key has ever been included in an archive or pushed to a repository, revoke/rotate it.
