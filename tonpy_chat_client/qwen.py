import os
from openai import OpenAI
client = OpenAI(
    api_key="sk-061fdeb4bb784fa2b097d4413ea6ac5f",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def chat_qwen(input_prompt):
    completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": input_prompt}]
    )
    return completion.choices[0].message.content