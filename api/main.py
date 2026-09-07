from fastapi import FastAPI

from api.schemas import QuestionRequest, QuestionResponse
from rag.pipeline import run_rag


app = FastAPI(
    title="RAG API",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=QuestionResponse)
def ask(request: QuestionRequest):

    result = run_rag(request.question)

    return QuestionResponse(
        answer=result["answer"],
        contexts=result["contexts"],
    )