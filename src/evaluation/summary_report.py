import csv
import os
from collections import defaultdict

from src.evaluation.evaluator import evaluate_all

LOG_PATH = "data/tool_call_log.csv"


def _load_tool_logs() -> list[dict]:
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH) as f:
        return list(csv.DictReader(f))


def print_summary_report() -> None:
    print("=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    eval_results = evaluate_all()
    correct_count = sum(1 for r in eval_results if r["is_correct"])
    print(f"\nAnswer quality: {correct_count}/{len(eval_results)} scenarios graded CORRECT")
    for r in eval_results:
        status = "PASS" if r["is_correct"] else "FAIL"
        print(f"  [{status}] {r['id']}")

    print("\n" + "=" * 60)
    print("OPERATIONAL METRICS")
    print("=" * 60)

    logs = _load_tool_logs()
    if not logs:
        print("\nNo tool call logs found yet.")
        return

    by_tool = defaultdict(list)
    for row in logs:
        by_tool[row["tool_name"]].append(row)

    for tool_name, rows in by_tool.items():
        successes = sum(1 for r in rows if r["success"] == "True")
        total = len(rows)
        latencies = [float(r["latency_ms"]) for r in rows]
        avg_latency = sum(latencies) / len(latencies)
        print(f"\n{tool_name}:")
        print(f"  Success rate: {successes}/{total}")
        print(f"  Average latency: {avg_latency:.1f}ms")


if __name__ == "__main__":
    print_summary_report()
