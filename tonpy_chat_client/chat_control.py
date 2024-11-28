import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-061fdeb4bb784fa2b097d4413ea6ac5f",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 这里应该处理聊天的信息，返回信息，目前只有通义的AI
# TODO 但感觉其实是要一直监听有没有信息来，所以这个方法是不靠谱的


def chat_with_individual(input_prompt):
    completion = client.chat.completions.create(
        model="qwen-turbo", messages=[{"role": "user", "content": input_prompt}]
    )
    return completion.choices[0].message.content
