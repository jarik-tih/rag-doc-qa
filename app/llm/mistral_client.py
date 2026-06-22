from ollama import Client

client = Client(
    host="https://localhost:11434"
)

def generate_answer(
        user_prompt: str,
        system_prompt: str,
):
    response = client.chat(
        model='mistral',
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            },
        ],
    )
    return response["message"]["content"]