import json
from langchain_ollama import ChatOllama
from app.embeddings.models import get_bge_embed_model
from ragas import (
    EvaluationDataset,
    SingleTurnSample,
    evaluate,
)

from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)

from rag.pipeline import run_rag
from ragas.run_config import RunConfig

model = get_bge_embed_model()

class RagasEmbeddingWrapper:

    def embed_documents(self, texts):
        return [
            model.get_text_embedding(text)
            for text in texts
        ]

    def embed_query(self, text):
        return model.get_query_embedding(text)


def load_test_dataset():

    with open(
        "../evaluation/dataset.json",
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def main():

    test_cases = load_test_dataset()

    samples = []

    evaluator_llm = ChatOllama(
        model="mistral",
        base_url="http://localhost:11434",
        temperature=0,
    )
    evaluator_embeddings = RagasEmbeddingWrapper()

    for item in test_cases:

        question = item["question"]
        reference = item["reference"]

        print(f"Evaluating: {question}")

        result = run_rag(question)

        sample = SingleTurnSample(
            user_input=question,
            retrieved_contexts=result["contexts"],
            response=result["answer"],
            reference=reference,
        )

        samples.append(sample)

    dataset = EvaluationDataset(
        samples=samples
    )

    metrics = [
        Faithfulness(),
        AnswerRelevancy(),
        ContextPrecision(),
        ContextRecall(),
    ]

    results = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=evaluator_llm,
        embeddings= evaluator_embeddings,
        run_config=RunConfig(max_workers=2, timeout=360),
    )

    print("\nEvaluation results:")
    print(results)


if __name__ == "__main__":
    main()