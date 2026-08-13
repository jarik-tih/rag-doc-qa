from app.retrieval.qdrant_store import QdrantStore

qdrant_store = QdrantStore(
    collection_name="recursive_bge",
)

def get_document_context(
    document_id: str,
    chunk_index: int,
    window: int = 2,
) -> dict:
    """
    Return an expanded context around a relevant chunk.

    The returned context contains the requested chunk
    and neighboring chunks from the same document.

    Args:
        document_id: ID of the source document.
        chunk_index: Index of the relevant chunk.
        window: Number of neighboring chunks to include
                before and after the target chunk.

    Returns:
        Expanded document context.
    """

    chunks = qdrant_store.get_document_context(
        document_id=document_id,
        chunk_index=chunk_index,
        window=window,
    )

    return {
        "document_id": document_id,
        "target_chunk_index": chunk_index,
        "window": window,
        "chunks": chunks,
    }