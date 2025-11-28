# Helper functions will be added later.
# src/utils.py

def strip_code_fences(text: str) -> str:
    """
    Remove leading/trailing Markdown code fences like ```python ... ```
    so we get pure Python code.
    """
    if not text:
        return text

    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        # Drop first line (``` or ```python)
        lines = lines[1:]
        # If last line is ``` drop it
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    return text
