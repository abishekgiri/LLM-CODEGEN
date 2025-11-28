import csv

from src.task_loader import load_tasks
from src.code_generator import generate_code
from src.test_runner import run_tests
from src.repair_loop import repair_code
from src.analyzer import analyze_results

# How many independent runs per task
N_RUNS = 5

RESULTS_CSV = "results/experiment_runs.csv"


def run_single_task(task, run_id: int):
    """
    Run one full pipeline (generate -> test -> optional repair)
    for a single task and a single run_id.
    Returns a dict with metrics for this run.
    """
    description = task["description"]
    func_name = task["func_name"]

    # 1) Initial generation
    code = generate_code(description)

    # 2) Initial tests
    initial_results = run_tests(code, task["tests"], func_name)
    initial_all_passed, _ = analyze_results(initial_results)

    # If everything passes, no repair needed
    if initial_all_passed:
        return {
            "run_id": run_id,
            "task_id": task["id"],
            "title": task["title"],
            "func_name": func_name,
            "initial_passed": True,
            "used_repair": False,
            "iterations": 0,
            "final_passed": True,   # same as initial
        }

    # 3) Run repair loop
    fixed_code, fixed_results, iters = repair_code(
        description,
        func_name,
        code,
        task["tests"],
        max_iters=3,
    )

    final_all_passed, _ = analyze_results(fixed_results)

    return {
        "run_id": run_id,
        "task_id": task["id"],
        "title": task["title"],
        "func_name": func_name,
        "initial_passed": False,
        "used_repair": True,
        "iterations": iters,
        "final_passed": final_all_passed,
    }


def main():
    tasks = load_tasks()
    fieldnames = [
        "run_id",
        "task_id",
        "title",
        "func_name",
        "initial_passed",
        "used_repair",
        "iterations",
        "final_passed",
    ]

    rows = []

    for run_id in range(1, N_RUNS + 1):
        print(f"\n=== RUN {run_id} ===")
        for task in tasks:
            print(f"  -> Task {task['id']}: {task['title']}")
            stats = run_single_task(task, run_id)
            rows.append(stats)

    # Write all results to CSV
    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n📊 Multi-run experiment saved to {RESULTS_CSV}")


if __name__ == "__main__":
    main()
