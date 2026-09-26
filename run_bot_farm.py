
import argparse
import csv
import json
from pathlib import Path

from botfarm.models import Persona, Scenario
from botfarm.orchestrator import run_farm

ROOT = Path(__file__).parent
CONFIG = ROOT / "config"
RESULTS = ROOT / "results"

def load_data():
    personas_raw = json.loads((CONFIG / "personas.json").read_text(encoding="utf-8"))
    scenarios_raw = json.loads((CONFIG / "scenarios.json").read_text(encoding="utf-8"))

    personas = [Persona(**p) for p in personas_raw]
    scenarios = [Scenario(**s) for s in scenarios_raw]
    return personas, scenarios

def save_results(results):
    RESULTS.mkdir(exist_ok=True)

    (RESULTS / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    fields = [
        "run_id", "scenario_id", "persona_id",
        "kyc_result", "root_cause_result",
        "resolution_result", "escalation_result",
        "overall_result", "failures"
    ]

    with (RESULTS / "summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in results:
            row = {k: r[k] for k in fields}
            row["failures"] = " | ".join(row["failures"])
            writer.writerow(row)

def print_summary(results):
    total = len(results)
    passed = sum(1 for r in results if r["overall_result"] == "PASS")
    failed = total - passed

    print("=" * 60)
    print("VOICEBOT QA BOT FARM")
    print("=" * 60)
    print(f"Total tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print(f"Pass rate   : {(passed / total * 100) if total else 0:.1f}%")
    print("=" * 60)

    for r in sorted(results, key=lambda x: (x["scenario_id"], x["persona_id"])):
        print(
            f'{r["scenario_id"]} | {r["persona_id"]} | '
            f'KYC={r["kyc_result"]} | '
            f'RootCause={r["root_cause_result"]} | '
            f'Resolution={r["resolution_result"]} | '
            f'Overall={r["overall_result"]}'
        )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--repeat", type=int, default=1)
    args = parser.parse_args()

    personas, scenarios = load_data()
    results = run_farm(personas, scenarios, workers=args.workers, repeat=args.repeat)
    save_results(results)
    print_summary(results)

if __name__ == "__main__":
    main()
