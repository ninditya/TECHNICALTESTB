from fastapi import FastAPI
from EmbeddingService import EmbeddingService
from DocumentStore import DocumentStore
from RagWorkflow import RagWorkflow
from Routes import create_router

app = FastAPI(title="Learning RAG Demo")

embedding_service = EmbeddingService()
document_store = DocumentStore(embedding_service)
rag_workflow = RagWorkflow(document_store)

app.include_router(
    create_router(rag_workflow, document_store)
)