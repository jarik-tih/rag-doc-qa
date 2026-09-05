from app.embeddings.models import get_bge_embed_model
from app.retrieval.qdrant_store import QdrantStore
from app.llm.utils import build_context, answer_question


store = QdrantStore(
    collection_name="recursive_bge"
)


def run_rag(question: str):
    model = get_bge_embed_model()

    query_embedding = model.get_text_embedding(question)

    results = store.search(
        query_embedding=query_embedding,
        top_k=5,
    )

    contexts = []

    for hit in results:

        payload = hit.payload

        document_id = payload["document_id"]
        chunk_index = payload["chunk_index"]

        expanded_chunks = store.get_document_context(
            document_id=document_id,
            chunk_index=chunk_index,
            window=2,
        )

        contexts.extend(
            chunk["text"]
            for chunk in expanded_chunks
        )

    contexts = list(dict.fromkeys(contexts))

    context = build_context(contexts)

    answer = answer_question(
        question,
        context,
    )

    return {
        "question": question,
        "contexts": contexts,
        "answer": answer,
    }