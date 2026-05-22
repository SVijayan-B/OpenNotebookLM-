from fastapi import APIRouter
from typing import List

from app.models.query import QueryRequest, QueryResponse, Source
from app.services.embedder import Embedder
from app.services.vector_store import FAISSVectorStore
from app.services.retriever import Retriever
from app.services.llm import OllamaLLM
from app.services.guardrails import Guardrails

router = APIRouter(prefix="/query", tags=["RAG Query"])

# -----------------------------
# SINGLETON SERVICES
# -----------------------------
embedder = Embedder(device=None)
vector_store = FAISSVectorStore()
retriever = Retriever(embedder, vector_store)
llm = OllamaLLM()


@router.post("", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    question = request.question
    question_lower = question.lower()

    # -----------------------------
    # Detect SUMMARY MODE
    # -----------------------------
    is_summary_query = any(
        kw in question_lower
        for kw in [
            "summary",
            "summarize",
            "overview",
            "what is this document",
            "what is this about",
        ]
    )

    # -----------------------------
    # RETRIEVAL
    # -----------------------------
    if is_summary_query:
        # 🔥 NotebookLM-style summary retrieval
        results = retriever.retrieve_for_summary(question)
    else:
        # 🔒 Strict factual retrieval
        results = retriever.retrieve(question)

    # -----------------------------
    # Guardrail: retrieval validation
    # -----------------------------
    if not results:
        refusal = Guardrails.refusal_response()
        return QueryResponse(**refusal)

    # -----------------------------
    # Build context
    # -----------------------------
    context = retriever.build_context(results)

    # -----------------------------
    # Generate answer
    # -----------------------------
    answer = llm.generate(
        question=question,
        context=context
    )

    # -----------------------------
    # Guardrail: answer validation
    # -----------------------------
    if not Guardrails.validate_answer(answer):
        refusal = Guardrails.refusal_response()
        return QueryResponse(**refusal)

    # -----------------------------
    # Build sources
    # -----------------------------
    sources: List[Source] = []
    for r in results:
        sources.append(
            Source(
                source=r["source"],
                page=r.get("page"),
                start_time=r.get("start_time"),
                end_time=r.get("end_time"),
                score=r["score"],
            )
        )

    return QueryResponse(
        answer=answer,
        sources=sources
    )
