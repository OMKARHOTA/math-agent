import os
from groq import Groq
from dotenv import load_dotenv
from groq.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_llm(prompt: str) -> str:
    messages = [
        ChatCompletionSystemMessageParam(
            role="system",
            content="You are a helpful AI assistant."
        ),
        ChatCompletionUserMessageParam(
            role="user",
            content=prompt
        )
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.2,
    )

    return response.choices[0].message.content