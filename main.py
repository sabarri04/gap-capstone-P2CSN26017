"""CLI entry point. Usage: python main.py samples/inputs/sample_ok.json"""
import argparse
import json
import sys
from pipeline import run_pipeline, load_incident, InputRejected

def main():
    parser = argparse.ArgumentParser(description="Sentinel evidence-gap investigation assistant")
    parser.add_argument("input_file", help="Path to an incident JSON file")
    args = parser.parse_args()
    try:
        # Reject malformed/empty/oversized input before entering the model pipeline.
        load_incident(args.input_file)
    except (InputRejected, OSError) as exc:
        print(f"Input rejected: {exc}", file=sys.stderr)
        print("error")
        return 2
    result = run_pipeline(args.input_file)
    if result["status"] == "ok":
        print(json.dumps(result["output"], ensure_ascii=False, indent=2))
        print("ok")
        return 0
    print(f"Analysis failed: {result['error']}", file=sys.stderr)
    print(result["status"])
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
