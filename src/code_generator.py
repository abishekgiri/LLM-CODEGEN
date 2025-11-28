from groq import Groq
from src.config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)

def generate_code(problem_description: str) -> str:
    prompt = f"""
You are an expert Python developer.

Write a correct, complete Python function for the following problem:

{problem_description}

Requirements:
- Use plain Python (no external libraries).
- Return ONLY valid Python code. No explanations, no markdown, no comments.
""".strip()

    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return resp.choices[0].message.content
