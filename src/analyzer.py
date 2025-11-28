# src/analyzer.py

def analyze_results(results):
    """
    Takes a list of test results from run_tests and returns:
      - all_passed: bool
      - summary: string describing failures/errors

    Each result dict has:
      - "input"
      - "expected"
      - ("output" OR "error")
    """
    all_passed = True
    issues = []

    for r in results:
        expected = r.get("expected")

        if "error" in r:
            # Special case: if we had encoded expected error types, we'd handle them here.
            # Currently, all tests in your advanced JSON expect normal values,
            # so any error counts as a failure.
            all_passed = False
            issues.append(f"Unexpected error for input {r['input']}: {r['error']}")
        else:
            if r["output"] != expected:
                all_passed = False
                issues.append(
                    f"Wrong output for input {r['input']}: got {r['output']}, expected {expected}"
                )

    summary = "\n".join(issues) if issues else "All tests passed."
    return all_passed, summary


def summarize_failures(results):
    """
    Build a detailed, line-by-line summary of failing tests
    for use in the repair prompt.

    Returns a multi-line string listing each failing or error case.
    """
    lines = []

    for r in results:
        expected = r.get("expected")

        if "error" in r:
            lines.append(
                f"- INPUT={r['input']} | expected={expected} | ERROR={r['error']}"
            )
        else:
            if r["output"] != expected:
                lines.append(
                    f"- INPUT={r['input']} | expected={expected} | got={r['output']}"
                )

    if not lines:
        return "All tests passed."

    return "\n".join(lines)
