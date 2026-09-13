from app.ai.ats_analyzer.context import ATSContext
from app.ai.ats_analyzer.representations import (
    ats_representation_builder,
)
from app.ai.embeddings.service import embedding_service
from app.ai.matching.similarity import (
    cosine_similarity,
)
from app.ai.matching.scoring import (
    normalize_semantic_similarity,
)


class ATSSemanticAnalyzer:
    """
    Calculates semantic relevance between a candidate's resume
    and the selected job.

    This component is responsible only for embedding generation
    and vector similarity. It does not calculate the final ATS
    score and does not call an LLM for qualitative analysis.
    """

    def __init__(self):
        self.representation_builder = ats_representation_builder
        self.embedding_service = embedding_service

    def calculate(
        self,
        context: ATSContext,
    ) -> float:
        resume_text, job_text = (
            self.representation_builder.build(context)
        )

        resume_embedding = self.embedding_service.embed_text(
            resume_text
        )

        job_embedding = self.embedding_service.embed_text(
            job_text
        )

        similarity = cosine_similarity(
            resume_embedding,
            job_embedding,
        )

        return normalize_semantic_similarity(
            similarity
        )


ats_semantic_analyzer = ATSSemanticAnalyzer()