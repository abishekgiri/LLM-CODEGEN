# src/static_analyzer.py

import subprocess
import tempfile
from typing import List, Dict


def run_static_analysis(code: str) -> List[Dict]:
    """
    Run flake8 on the given Python code string.
    Returns a list of issue dicts:
      { "code": str, "line": int, "col": int, "message": str }

    If flake8 is not installed, returns an empty list.
    """
    try:
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as tmp:
            tmp.write(code)
            tmp.flush()
            tmp_name = tmp.name

        # Use simple, parseable format: CODE:LINE:COL:MESSAGE
        result = subprocess.run(
            ["flake8", tmp_name, "--format=%(code)s:%(line)d:%(col)d:%(text)s"],
            capture_output=True,
            text=True,
        )

        if result.returncode not in (0, 1):  # 0 = no issues, 1 = issues, others = errors
            return []

        issues = []
        for line in result.stdout.splitlines():
            parts = line.split(":", 3)
            if len(parts) != 4:
                continue
            code_str, line_str, col_str, message = parts
            try:
                issues.append(
                    {
                        "code": code_str.strip(),
                        "line": int(line_str),
                        "col": int(col_str),
                        "message": message.strip(),
                    }
                )
            except ValueError:
                continue

        return issues

    except FileNotFoundError:
        # flake8 not installed
        return []
