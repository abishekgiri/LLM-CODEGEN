# analyze_experiments_advanced.py

import csv
from collections import defaultdict

CSV_PATH = "results/advanced_experiment_runs.csv"


def main():
    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # stats[(task_id, strategy)] -> aggregations
    stats = defaultdict(
        lambda: {
            "title": None,
            "func_name": None,
            "strategy": None,
            "runs": 0,
            "initial_passed_count": 0,
            "final_passed_count": 0,
            "repair_used_count": 0,
            "total_iterations_when_repair_used": 0,
            "sum_initial_static_issues": 0,
            "sum_final_static_issues": 0,
        }
    )

    for row in rows:
        key = (row["task_id"], row["strategy"])
        s = stats[key]

        s["title"] = row["title"]
        s["func_name"] = row["func_name"]
        s["strategy"] = row["strategy"]
        s["runs"] += 1

        initial_passed = (row["initial_passed"] == "True")
        final_passed = (row["final_passed"] == "True")
        used_repair = (row["used_repair"] == "True")
        iterations = int(row["iterations"])

        s["sum_initial_static_issues"] += int(row["initial_static_issues"])
        s["sum_final_static_issues"] += int(row["final_static_issues"])

        if initial_passed:
            s["initial_passed_count"] += 1
        if final_passed:
            s["final_passed_count"] += 1
        if used_repair:
            s["repair_used_count"] += 1
            s["total_iterations_when_repair_used"] += iterations

    print(f"Analysis of strategies from {CSV_PATH}\n")

    # Group by task so we can print strategies side-by-side
    tasks = sorted(set(task_id for (task_id, _) in stats.keys()), key=int)

    for task_id in tasks:
        # Collect all strategies for this task
        task_stats = [v for (tid, _), v in stats.items() if tid == task_id]
        # Sort by strategy name for stable output
        task_stats.sort(key=lambda x: x["strategy"])

        title = task_stats[0]["title"]
        func_name = task_stats[0]["func_name"]

        print(f"Task {task_id}: {title}  (func: {func_name})")

        for s in task_stats:
            runs = s["runs"]
            init_rate = s["initial_passed_count"] / runs
            final_rate = s["final_passed_count"] / runs
            repair_rate = s["repair_used_count"] / runs
            avg_iters = (
                s["total_iterations_when_repair_used"] / s["repair_used_count"]
                if s["repair_used_count"] > 0
                else 0.0
            )
            avg_initial_static = s["sum_initial_static_issues"] / runs
            avg_final_static = s["sum_final_static_issues"] / runs

            print(f"  Strategy: {s['strategy']}")
            print(f"    Runs: {runs}")
            print(f"    Initial pass rate : {init_rate:.2f}")
            print(f"    Final pass rate   : {final_rate:.2f}")
            print(f"    Repair used rate  : {repair_rate:.2f}")
            print(f"    Avg iters (when repair used): {avg_iters:.2f}")
            print(f"    Avg flake8 issues (initial): {avg_initial_static:.2f}")
            print(f"    Avg flake8 issues (final)  : {avg_final_static:.2f}")
        print("-" * 70)


if __name__ == "__main__":
    main()
