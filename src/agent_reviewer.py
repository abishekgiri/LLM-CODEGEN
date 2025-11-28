# src/agent_reviewer.py

from groq import Groq
from src.config import GROQ_API_KEY, MODEL_NAME
from src.utils import strip_code_fences

client = Groq(api_key=GROQ_API_KEY)


def review_code(problem_description: str, func_name: str, code: str) -> str:
    """
    LLM 'Reviewer' agent:
    - Takes the problem description + current code
    - Returns an improved version of the full code (same func_name).
    """

    prompt = f"""
You are a senior Python code reviewer.

Problem:
{problem_description}

Current implementation of `{func_name}`:
{code}

Your job:
- Find possible bugs, edge-case failures, or logical mistakes.
- Fix them.
- Keep the function name exactly `{func_name}`.
- Return ONLY the corrected Python code (no comments, no explanations, no markdown).
    """.strip()

    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    improved = strip_code_fences(resp.choices[0].message.content)
    return improved
