import json

def load_chunks(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_embeddings(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)