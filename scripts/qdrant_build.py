from app.retrieval.qdrant_store import QdrantStore
from app.retrieval.utils import  load_embeddings
from app.embeddings.utils import load_chunks

store = QdrantStore(
    collection_name="recursive_bge"
)

chunks = load_chunks("../data/processed/recursive_nodes.json")
embeddings = load_embeddings("../data/processed/bge_embeddings.json")

print(len(chunks))
print(len(embeddings))
print(len(embeddings[0]))

BATCH_SIZE = 500
for start in range(0, len(chunks), BATCH_SIZE):
    end = min(start + BATCH_SIZE, len(chunks))

    store.add_documents(
        ids=[chunk["id"] for chunk in chunks[start:end]],
        texts=[chunk["text"] for chunk in chunks[start:end]],
        embeddings=embeddings[start:end],
        metadatas=[chunk["metadata"] for chunk in chunks[start:end]],
    )

    print(f"Uploaded {end}/{len(chunks)}")