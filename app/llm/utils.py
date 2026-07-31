from app.llm.prompts import SYSTEM_PROMPT
from app.llm.mistral_client import generate_answer

def build_context(search_results):
    return "\n\n".join(
        chunk["text"]
        for chunk in search_results
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