from src.metrics import save_experiment_log, summarize_task_results
from src.task_loader import load_tasks
from src.code_generator import generate_code
from src.test_runner import run_tests
from src.repair_loop import repair_code
from src.analyzer import analyze_results

def print_results(label, results):
    print(label)
    for r in results:
        expected = r.get("expected")

        if "error" in r:
            # ✅ Expected division-by-zero error = PASS
            if expected == "error_div_zero" and "division by zero" in r["error"]:
                print(f"✓ PASS | input={r['input']} | expected=division by zero error | got error='{r['error']}'")
            else:
                print(f"❌ Error for input {r['input']}: {r['error']}")
        else:
            if expected == "error_div_zero":
                print(f"✗ FAIL | input={r['input']} | expected division-by-zero error but got value {r['output']}")
            else:
                status = "✓ PASS" if r["output"] == expected else "✗ FAIL"
                print(f"{status} | input={r['input']} | output={r['output']} | expected={expected}")


def main():
    tasks = load_tasks()
    experiment_log = []

    for task in tasks:
        print(f"\n===== TASK {task['id']}: {task['title']} =====")

        description = task["description"]
        func_name = task["func_name"]

        # 1) Initial generation
        code = generate_code(description)
        print("\nGenerated Code:")
        print(code)

        # 2) Initial tests
        results = run_tests(code, task["tests"], func_name)
        print_results("\nINITIAL TEST RESULTS:", results)

        # Decide if we need repair using analyzer
        initial_all_passed, _ = analyze_results(results)

        if initial_all_passed:
            # Log and continue
            task_summary = summarize_task_results(
                task,
                initial_results=results,
                final_results=None,
                iterations=0,
            )
            experiment_log.append(task_summary)
            continue

        # 3) Attempt repair loop
        print("\n⚙️ Some tests failed — attempting automated repair...")
        fixed_code, fixed_results, iters = repair_code(
            description,
            func_name,
            code,
            task["tests"],
            max_iters=3,
        )

        print(f"\nAfter repair (iterations={iters}):")
        print(f"\nRepaired Code:\n{fixed_code}")
        print_results("\nFINAL TEST RESULTS:", fixed_results)

        # Log repaired task
        task_summary = summarize_task_results(
            task,
            initial_results=results,
            final_results=fixed_results,
            iterations=iters,
        )
        experiment_log.append(task_summary)

    # After all tasks, save log
    save_experiment_log(experiment_log)
    print("\n📊 Experiment log saved to results/experiment_log.json")

if __name__ == "__main__":
    main()
