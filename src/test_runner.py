import subprocess
import tempfile
import json

def run_tests(code: str, tests: list, func_name: str):
    """
    Executes generated python code and runs the provided tests on the specified function.

    tests: list of dicts with:
      - "input": JSON-serializable value or list/tuple of args
      - "expected": JSON-serializable value, or special string for errors (e.g. "error_div_zero")
      - optional "multi_args": bool, if True then input list is expanded as *args
    """

    test_script = code + "\n\n" + """
import json
results = []
"""

    for t in tests:
        input_value = t["input"]
        expected_value = t["expected"]
        multi_args = t.get("multi_args", False)

        input_literal = json.dumps(input_value)
        expected_literal = json.dumps(expected_value)
        multi_literal = "True" if multi_args else "False"

        test_script += f"""
try:
    args = {input_literal}
    if {multi_literal} and isinstance(args, list):
        output = {func_name}(*args)
    else:
        output = {func_name}(args)
    results.append({{"input": {input_literal}, "output": output, "expected": {expected_literal}}})
except Exception as e:
    results.append({{"error": str(e), "input": {input_literal}, "expected": {expected_literal}}})
"""

    test_script += """
print(json.dumps(results))
"""

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
        temp.write(test_script.encode())
        temp.flush()

        result = subprocess.run(
            ["python3", temp.name],
            capture_output=True,
            text=True
        )

    try:
        parsed = json.loads(result.stdout)
        # If parsed is a dict, wrap into list
        if isinstance(parsed, dict):
            return [parsed]
        return parsed
    except Exception:
        # On total failure, return a single-error list
        return [{"error": result.stderr, "input": None, "expected": None}]
