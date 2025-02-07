import os
from openai import OpenAI

api = "YOUR_API"
client = OpenAI(
    api_key=api,
    base_url="YOUR_BASE",
)


def chatai(input_prompt):
    try:
        completion = client.chat.completions.create(
            model="qwen-turbo", messages=[{"role": "user", "content": input_prompt}]
        )
        return completion.choices[0].message.content
    except:
        return "API not configured."
