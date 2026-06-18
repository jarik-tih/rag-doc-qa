from app.retrieval.qdrant_store import QdrantStore
from app.retrieval.utils import  load_embeddings
from app.embeddings.utils import load_chunks

store = QdrantStore(
    collection_name="recursive_bge"
)

chunks = load_chunks("../data/processed/recursive_nodes.json")
embeddings = load_embeddings("../data/processed/bge_embeddings.json")

store.add_documents(
    ids=[chunk["id"] for chunk in chunks],
    texts=[chunk["text"] for chunk in chunks],
    embeddings=embeddings,
    metadatas=[chunk["metadata"] for chunk in chunks],
)
