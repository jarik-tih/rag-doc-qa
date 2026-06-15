def search(collection, query_embedding, top_k=5):
    return collection.search(
        query_embedding=[query_embedding],
        n_results=top_k,
    )