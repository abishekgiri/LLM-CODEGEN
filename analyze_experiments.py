import csv
from collections import defaultdict

CSV_PATH = "results/experiment_runs.csv"


def main():
    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Group stats by task_id
    stats = defaultdict(lambda: {
        "title": None,
        "func_name": None,
        "runs": 0,
        "initial_passed_count": 0,
        "final_passed_count": 0,
        "repair_used_count": 0,
        "total_iterations_when_repair_used": 0,
    })

    for row in rows:
        task_id = row["task_id"]
        s = stats[task_id]

        s["title"] = row["title"]
        s["func_name"] = row["func_name"]
        s["runs"] += 1

        initial_passed = row["initial_passed"] == "True"
        final_passed = row["final_passed"] == "True"
        used_repair = row["used_repair"] == "True"
        iterations = int(row["iterations"])

        if initial_passed:
            s["initial_passed_count"] += 1
        if final_passed:
            s["final_passed_count"] += 1
        if used_repair:
            s["repair_used_count"] += 1
            s["total_iterations_when_repair_used"] += iterations

    # Pretty-print summary
    print(f"Analysis of {len(stats)} tasks from {CSV_PATH}\n")

    for task_id, s in stats.items():
        runs = s["runs"]
        init_rate = s["initial_passed_count"] / runs
        final_rate = s["final_passed_count"] / runs
        repair_rate = s["repair_used_count"] / runs
        avg_iters = (
            s["total_iterations_when_repair_used"] / s["repair_used_count"]
            if s["repair_used_count"] > 0 else 0.0
        )

        print(f"Task {task_id}: {s['title']}  (func: {s['func_name']})")
        print(f"  Runs: {runs}")
        print(f"  Initial pass rate : {init_rate:.2f}")
        print(f"  Final pass rate   : {final_rate:.2f}")
        print(f"  Repair used rate  : {repair_rate:.2f}")
        print(f"  Avg iters (when repair used): {avg_iters:.2f}")
        print("-" * 60)


if __name__ == "__main__":
    main()
