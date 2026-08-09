from app.retrieval.qdrant_store import QdrantStore
from app.embeddings.models import BGE_EMBED_MODEL


store = QdrantStore(
    collection_name="recursive_bge",
)


def search_documents(
    query: str,
    top_k: int = 5,
):
    query_embedding = BGE_EMBED_MODEL.get_text_embedding(query)

    results = store.search(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    return [
        {
            "id": str(result.id),
            "score": result.score,
            "text": result.payload["text"],
            "metadata": result.payload["metadata"],
        }
        for result in results
    ]