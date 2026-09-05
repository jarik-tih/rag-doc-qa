from app.llm.utils import (
    build_context,
    answer_question,
)

from app.retrieval.qdrant_store import QdrantStore
from app.embeddings.models import get_bge_embed_model


store = QdrantStore(
    collection_name="recursive_bge",
)

model = get_bge_embed_model()
question = input("Question: ")

query_embedding = (
    model.get_text_embedding(question)
)

results = store.search(
    query_embedding=query_embedding,
    top_k=5,
)

context_chunks = []
seen_chunks = set()

for hit in results:

    payload = hit.payload

    document_id = payload["document_id"]
    chunk_index = payload["chunk_index"]

    expanded_chunks = store.get_document_context(
        document_id=document_id,
        chunk_index=chunk_index,
        window=2,
    )

    for chunk in expanded_chunks:

        chunk_id = chunk["chunk_id"]

        if chunk_id not in seen_chunks:

            seen_chunks.add(chunk_id)

            context_chunks.append(
                chunk["text"]
            )

context = build_context(
    context_chunks
)

answer = answer_question(
    question,
    context,
)


print(f"\nAnswer: {answer}")