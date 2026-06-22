from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    HnswConfigDiff,
)

class QdrantStore:

    def __init__(
            self,
            collection_name:str,
            vector_size:int=768,
    ):

        self.client = QdrantClient(
            host="local_host",
            port= 6333,
        )

        self.collection_name = collection_name
        collections = self.client.get_collections()

        existing = [
            c.name
            for c in collections.collections
        ]

        if collection_name not in existing:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
                hnsw_config=HnswConfigDiff(
                    m=16,
                    ef_construct=100,
                ),
            )

    def add_documents(
            self,
            ids,
            texts,
            embeddings,
            metadatas,
    ):
        points = []
        for idx, text, embedding, metadata in zip(
            ids,
            texts,
            embeddings,
            metadatas,
        ):

            points.append(
                PointStruct(
                    id=idx,
                    vector=embedding,
                    payload={
                        "text": text,
                        "metadata": metadata,
                    },
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(
            self,
            query_embedding,
            top_k=5,
    ):

        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
        )