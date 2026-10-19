"""
Optional adapter for Ragas (Retrieval Augmented Generation Assessment) evaluation framework.

This adapter provides lazy-loaded integration with Ragas metrics (faithfulness, answer_relevancy,
context_precision, context_recall). It remains an optional offline developer dependency and is
never required in the production request path.
"""

from typing import Any


def is_ragas_available() -> bool:
    """Checks if ragas and its required dataset dependencies are importable."""
    try:
        import datasets  # noqa: F401
        import ragas  # noqa: F401
        return True
    except ImportError:
        return False


class CandidateEvidenceRagasAdapter:
    """
    Adapter converting Hirely's Candidate Resume Evidence evaluation results
    into Ragas-compatible datasets for automated LLM-as-a-judge scoring.
    """

    def __init__(self, metrics: list[Any] | None = None):
        if not is_ragas_available():
            raise ImportError(
                "Ragas evaluation dependencies are not installed in the current environment. "
                "To enable Ragas evaluations, install optional dev dependencies: pip install ragas datasets."
            )

        from ragas.metrics import (  # type: ignore
            answer_relevancy,
            context_precision,
            context_recall,
            faithfulness,
        )

        self.metrics = metrics or [
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ]

    def build_dataset_dict(self, eval_cases_data: list[dict[str, Any]]) -> dict[str, list[Any]]:
        """
        Converts standardized evaluation case data into Ragas dataset format.

        Schema expected by Ragas:
        - question: str
        - contexts: list[str]
        - answer: str
        - ground_truth: str
        """
        questions: list[str] = []
        contexts: list[list[str]] = []
        answers: list[str] = []
        ground_truths: list[str] = []

        for item in eval_cases_data:
            questions.append(item.get("question", ""))
            contexts.append(item.get("contexts", []))
            answers.append(item.get("answer", ""))
            ground_truths.append(item.get("ground_truth", ""))

        return {
            "question": questions,
            "contexts": contexts,
            "answer": answers,
            "ground_truth": ground_truths,
        }

    def evaluate_cases(self, eval_cases_data: list[dict[str, Any]]) -> dict[str, float]:
        """
        Executes Ragas evaluation against prepared cases.
        """
        from datasets import Dataset  # type: ignore
        from ragas import evaluate  # type: ignore

        data_dict = self.build_dataset_dict(eval_cases_data)
        dataset = Dataset.from_dict(data_dict)
        results = evaluate(dataset=dataset, metrics=self.metrics)
        return dict(results)
