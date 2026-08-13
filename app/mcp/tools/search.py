from app.retrieval.qdrant_store import QdrantStore
from app.embeddings.generator import generate_bge_embeddings

qdrant_store = QdrantStore(
    collection_name="recursive_bge",
)


def search(
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Search the document collection using
    semantic vector search.

    Args:
        query: Natural language question.
        top_k: Number of relevant chunks to return.

    Returns:
        A list of relevant document chunks.
    """

    query_embedding = generate_bge_embeddings(query)

    results = qdrant_store.search(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    response = []

    for result in results:

        payload = result.payload

        response.append(
            {
                "chunk_id": str(result.id),
                "score": result.score,
                "document_id": payload["document_id"],
                "chunk_index": payload["chunk_index"],
                "text": payload["text"],
                "metadata": payload.get(
                    "metadata",
                    {},
                ),
            }
        )

    return response