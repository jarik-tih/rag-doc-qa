import os
from qdrant_client import QdrantClient
from uuid import uuid4

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    HnswConfigDiff,
)

class QdrantStore:

    def __init__(
            self,
            collection_names:list[str],
            vector_size:int=768,
    ):

        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))

        self.client = QdrantClient(
            host=qdrant_host,
            port=qdrant_port,
        )

        self.collection_names = collection_names
        collections = self.client.get_collections()

        existing = {
            c.name
            for c in collections.collections
        }

        for collection_name in collection_names:
            if collection_names not in existing:
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

    def _validate_collection(self, collection_name: str):

        if collection_name not in self.collection_names:
            raise ValueError(
                f"Unknown collection: {collection_name}"
            )

    def add_documents(
            self,
            collection_name: str,
            ids,
            texts,
            embeddings,
            metadatas,
    ):
        self._validate_collection(collection_name)

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
            collection_name=collection_name,
            points=points,
        )

    def add_point(
        self,
        collection_name: str,
        question: str,
        embedding: list[float],
        answer: str,
        contexts: list[str],
    ):
        point = PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "question": question,
                "answer": answer,
                "contexts": contexts,
            },
        )

        self.client.upsert(
            collection_name=collection_name,
            points=[point],
        )

    def search(
            self,
            collection_name: str,
            query_embedding,
            top_k=5,
    ):
        self._validate_collection(collection_name)

        response = self.client.query_points(
            collection_name=collection_name,
            query=query_embedding,
            limit=top_k,
        )

        return response.points

    def get_document_context(
            self,
            collection_name: str,
            document_id: str,
            chunk_index: int,
            window: int = 2,
    ):
        self._validate_collection(collection_name)

        results = self.client.scroll(
            collection_name=collection_name,
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