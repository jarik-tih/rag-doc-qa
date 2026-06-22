from app.llm.utils import (
    build_context,
    answer_question,
)
from app.retrieval.qdrant_store import QdrantStore
from app.embeddings.models import BGE_EMBED_MODEL

store = QdrantStore(
    collection_name="recursive_bge",
)

question = input("Question: ")

query_embedding = (
    BGE_EMBED_MODEL.get_text_embedding(question)
)

results = store.search(
    query_embedding=query_embedding,
)

context_chunks = [
    hit.payload["text"]
    for hit in results
]

answer = answer_question(question, build_context(context_chunks))

print(f"\nAnswer:{answer}")
