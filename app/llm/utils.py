from app.llm.prompts import SYSTEM_PROMPT
from app.llm.mistral_client import generate_answer

def build_context(chunks):
    if len(chunks) == 0:
        return ""

    if isinstance(chunks[0], str):
        return "\n\n".join(chunks)

    return "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

def answer_question(
        question: str,
        context: str
):
    prompt = f"""
Context: {context}
Question: {question}
"""

    return generate_answer(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
    )