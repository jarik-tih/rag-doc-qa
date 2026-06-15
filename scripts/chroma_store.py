import chromadb

from app.retrieval.utils import(
    add_documents,
    load_embeddings
)
from app.embeddings.utils import load_chunks

client = chromadb.PersistentClient(
    path="../chroma_db"
)

chunks = load_chunks("../data/processed/recursive_nodes.json")
collection = client.get_or_create_collection(
    name="info_ML"
)

embeddings = load_embeddings("../data/processed/bge_embeddings.json")
add_documents(
    collection,
    chunks,
    embeddings
)