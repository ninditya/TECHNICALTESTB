from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

class DocumentStore:
    def __init__(self, embedding_service):
        self.embedding_service = embedding_service
        self.docs_memory: List[str] = []

        self.client = None
        self.use_qdrant = False

        self._init_qdrant()

    def _init_qdrant(self):
        """Initialize Qdrant client and recreate collection"""
        try:
            self.client = QdrantClient("http://localhost:6333")
            self.client.recreate_collection(
                collection_name="demo_collection",
                vectors_config=VectorParams(size=128, distance=Distance.COSINE)
            )
            self.use_qdrant = True
            print(f"✅ Qdrant connected ready")
        except Exception as e:
            print(f"⚠️ Qdrant not available. Falling back to in-memory list.")
            self.use_qdrant = False

    def add_document(self, text: str) -> int:
        embedding = self.embedding_service.embed(text)
        doc_id = len(self.docs_memory)
        payload = {"text": text}

        if self.use_qdrant:
            self.client.upsert(
                collection_name="demo_collection",
                points=[PointStruct(id=doc_id, vector=embedding, payload=payload)]
            )
        else:
            self.docs_memory.append(text)

        return doc_id

    def search(self, query: str, limit: int = 2) -> List[str]:
        embedding = self.embedding_service.embed(query)

        if self.use_qdrant:
            hits = self.client.search(collection_name="demo_collection", query_vector=embedding, limit=limit)
            return [hit.payload["text"] for hit in hits]

        results = [doc for doc in self.docs_memory if query.lower() in doc.lower()]
        if not results and self.docs_memory:
            return [self.docs_memory[0]]
        return results