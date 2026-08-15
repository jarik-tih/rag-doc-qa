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
            host="localhost",
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
                        "document_id": metadata["document_id"],
                        "chunk_index": metadata["chunk_index"],
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

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=top_k,
        )

        return response.points

    def get_document_context(
            self,
            document_id: str,
            chunk_index: int,
            window: int = 2,
    ):

        results = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {
                        "key": "document_id",
                        "match": {
                            "value": document_id,
                        },
                    },
                ],
            },
            limit=100,
            with_payload=True,
            with_vectors=False,
        )[0]

        start = max(
            0,
            chunk_index - window,
            )
        end = chunk_index + window

        chunks = []

        for point in results:

            payload = point.payload

            index = payload["chunk_index"]

            if start <= index <= end:
                chunks.append(
                    {
                        "chunk_id": str(point.id),
                        "chunk_index": index,
                        "text": payload["text"],
                        "metadata": payload.get(
                            "metadata",
                            {},
                        ),
                    }
                )

        chunks.sort(
            key=lambda chunk: chunk["chunk_index"]
        )

        return chunks