import json

def load_embeddings(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def add_documents(collection, chunks, embeddings):
    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        embeddings=embeddings,
    )
