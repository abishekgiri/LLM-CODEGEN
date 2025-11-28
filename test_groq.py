import os
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
print("Key length:", len(api_key) if api_key else "None")

client = Groq(api_key=api_key)

resp = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Say hi in one word"}
    ],
)

print("Model:", resp.model)
print("Response:", resp.choices[0].message.content)
