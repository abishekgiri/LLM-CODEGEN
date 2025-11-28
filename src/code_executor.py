import subprocess
import tempfile

def run_python_code(code, timeout=3):
    # Create temp file
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
        temp.write(code.encode())
        temp.flush()

        try:
            result = subprocess.run(
                ["python3", temp.name],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return None, "Timeout Error"
