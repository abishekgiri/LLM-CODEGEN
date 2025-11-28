# run_experiments_advanced.py

import csv

from src.task_loader import load_tasks
from src.code_generator import generate_code
from src.test_runner import run_tests
from src.repair_loop import repair_code
from src.analyzer import analyze_results
from src.agent_reviewer import review_code
from src.static_analyzer import run_static_analysis

# How many independent runs per (task, strategy)
N_RUNS = 5

RESULTS_CSV = "results/advanced_experiment_runs.csv"

# Define different experiment strategies
STRATEGIES = [
    {
        "name": "no_repair",
        "use_repair": False,
        "max_iters": 0,
    },
    {
        "name": "repair_3",
        "use_repair": True,
        "max_iters": 3,
    },
    {
        "name": "repair_5",
        "use_repair": True,
        "max_iters": 5,
    },
    {
        "name": "review_then_repair_3",
        "use_repair": True,
        "max_iters": 3,
        "use_reviewer": True,  # pipeline: Coder -> Reviewer -> Tests -> Repair
    },
]


def run_single_task_with_strategy(task, run_id: int, strategy: dict):
    """
    Run one full pipeline (generate -> optional review -> test -> optional repair)
    for a single task, a single run_id, and a specific strategy.

    Returns a dict with metrics for this (task, run, strategy).
    """
    description = task["description"]
    func_name = task["func_name"]

    # 1) Initial generation by "Coder" agent
    code = generate_code(description)

    # Optional: second "Reviewer" agent pass before tests
    if strategy.get("use_reviewer"):
        code = review_code(description, func_name, code)

    # Static analysis on initial code
    initial_static_issues = len(run_static_analysis(code))

    # 2) Initial tests
    initial_results = run_tests(code, task["tests"], func_name)
    initial_all_passed, _ = analyze_results(initial_results)

    # Case A: strategy does not use repair OR everything already passed
    if (not strategy["use_repair"]) or initial_all_passed:
        final_static_issues = initial_static_issues

        return {
            "strategy": strategy["name"],
            "run_id": run_id,
            "task_id": task["id"],
            "title": task["title"],
            "func_name": func_name,
            "initial_passed": initial_all_passed,
            "used_repair": False,
            "iterations": 0,
            "final_passed": initial_all_passed,
            "initial_static_issues": initial_static_issues,
            "final_static_issues": final_static_issues,
        }

    # Case B: use repair and initial did NOT pass
    try:
        fixed_code, fixed_results, iters = repair_code(
            description,        # problem_description
            func_name,
            code,               # initial_code
            task["tests"],
            max_iters=strategy["max_iters"],
        )

        final_all_passed, _ = analyze_results(fixed_results)

        # Static analysis on final code
        final_static_issues = len(run_static_analysis(fixed_code))

        return {
            "strategy": strategy["name"],
            "run_id": run_id,
            "task_id": task["id"],
            "title": task["title"],
            "func_name": func_name,
            "initial_passed": False,
            "used_repair": True,
            "iterations": iters,
            "final_passed": final_all_passed,
            "initial_static_issues": initial_static_issues,
            "final_static_issues": final_static_issues,
        }

    except Exception as e:
        # Defensive: if the repair pipeline itself crashes,
        # record a failed run instead of aborting the whole experiment.
        print(
            f"    !! Repair failed for task {task['id']} run {run_id} "
            f"under strategy {strategy['name']}: {e}"
        )

        return {
            "strategy": strategy["name"],
            "run_id": run_id,
            "task_id": task["id"],
            "title": task["title"],
            "func_name": func_name,
            "initial_passed": False,
            "used_repair": True,
            "iterations": 0,
            "final_passed": False,
            "initial_static_issues": initial_static_issues,
            "final_static_issues": initial_static_issues,
        }


def main():
    tasks = load_tasks()

    fieldnames = [
        "strategy",
        "run_id",
        "task_id",
        "title",
        "func_name",
        "initial_passed",
        "used_repair",
        "iterations",
        "final_passed",
        "initial_static_issues",
        "final_static_issues",
    ]

    rows = []

    for strategy in STRATEGIES:
        print(f"\n=== STRATEGY: {strategy['name']} ===")
        for run_id in range(1, N_RUNS + 1):
            print(f"  RUN {run_id}")
            for task in tasks:
                print(f"    -> Task {task['id']}: {task['title']}")
                stats = run_single_task_with_strategy(task, run_id, strategy)
                rows.append(stats)

    # Write all results to CSV
    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n📊 Advanced multi-strategy experiment saved to {RESULTS_CSV}")


if __name__ == "__main__":
    main()
