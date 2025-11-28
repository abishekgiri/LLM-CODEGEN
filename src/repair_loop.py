# src/repair_loop.py

from groq import Groq

from src.config import GROQ_API_KEY, MODEL_NAME
from src.test_runner import run_tests
from src.analyzer import analyze_results, summarize_failures
from src.static_analyzer import run_static_analysis


client = Groq(api_key=GROQ_API_KEY)


def repair_code(
    problem_description: str,
    func_name: str,
    initial_code: str,
    tests: list,
    max_iters: int = 3,
):
    """
    Iteratively repairs code using BOTH test feedback and static-analysis feedback.

    Args:
        problem_description: Natural language description of the task.
        func_name: Name of the function that must be implemented (and preserved).
        initial_code: First version of the code from the LLM.
        tests: List of test-case dicts (input/expected/etc.).
        max_iters: Maximum number of repair iterations.

    Returns:
        (final_code: str, final_results: list[dict], iterations_used: int)
    """
    current_code = initial_code
    iterations = 0

    for i in range(max_iters):
        iterations = i + 1

        # 1) Run tests on current version
        results = run_tests(current_code, tests, func_name)
        all_passed, _ = analyze_results(results)

        # 2) Collect detailed failure info (even if we might stop)
        failure_details = summarize_failures(results)

        # 3) Run static analysis (flake8) on current version
        static_issues = run_static_analysis(current_code)
        static_summary = (
            "\n".join(static_issues) if static_issues else "No static-analysis issues found."
        )

        # 4) If tests pass and no static issues, we are done
        if all_passed and not static_issues:
            return current_code, results, iterations

        # 5) Build a rich repair prompt using both sources
        prompt = f"""
You are an expert Python developer.

You wrote the following code for this problem:

Problem:
{problem_description}

Current code:
{current_code}

The unit tests produced the following failing cases (if any):
{failure_details}

The static analysis (flake8) reported:
{static_summary}

Please provide a corrected version of the full Python code.

Requirements:
- Keep the function name exactly `{func_name}`.
- Fix ALL failing tests.
- Address any static-analysis issues if possible (e.g., unused variables, obvious style problems).
- Return ONLY valid Python code. No explanations, no markdown, no comments.
        """.strip()

        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        current_code = resp.choices[0].message.content

    # After max_iters, run tests one more time and return whatever we have
    final_results = run_tests(current_code, tests, func_name)
    return current_code, final_results, iterations
