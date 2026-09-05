from app.ai.matching.explanation import MatchExplanation, MatchExplanationInput
from app.ai.matching.explanation_prompt import ExplanationPromptBuilder
from app.ai.services.gemini_service import GeminiService


class MatchExplanationService:
    def __init__(
        self,
        gemini_service: GeminiService,
        prompt_builder: ExplanationPromptBuilder,
    ):
        self.gemini_service = gemini_service
        self.prompt_builder = prompt_builder

    def explain(
        self,
        data: MatchExplanationInput,
    ) -> MatchExplanation:
        prompt = self.prompt_builder.build(data)

        return self.gemini_service.generate_structured(
            prompt=prompt,
            response_schema=MatchExplanation,
        )

match_explanation_service = MatchExplanationService(
    gemini_service=GeminiService(),
    prompt_builder=ExplanationPromptBuilder(),
)