import json
import os


def save_experiment_log(log, path="results/experiment_log.json"):
    # Make sure results directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump(log, f, indent=2)


def summarize_task_results(task, initial_results, final_results=None, iterations=0):
    """
    Build a compact dict summarizing one task run.
    """
    def all_passed(results):
        for r in results:
            expected = r.get("expected")
            if "error" in r:
                # Special case: expected division-by-zero
                if expected == "error_div_zero" and "division by zero" in r["error"]:
                    continue
                else:
                    return False
            else:
                if expected == "error_div_zero":
                    return False
                if r["output"] != expected:
                    return False
        return True

    summary = {
        "task_id": task["id"],
        "title": task["title"],
        "func_name": task["func_name"],
        "initial_passed": all_passed(initial_results),
        "used_repair": final_results is not None,
        "iterations": iterations if final_results is not None else 0,
        "final_passed": all_passed(final_results) if final_results is not None else None,
    }

    return summary
