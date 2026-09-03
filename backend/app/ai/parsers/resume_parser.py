from app.ai.parsers.schemas import ResumeData
from app.ai.services.gemini_service import gemini_service


class ResumeParserService:
    def __init__(self, ai_service=gemini_service):
        self.ai_service = ai_service

    def parse(self, resume_text: str) -> ResumeData:
        prompt = f"""
        Extract structured candidate information from the following resume.

        Return only information explicitly present in the resume.
        Do not invent or infer missing information.

        Resume:
        {resume_text}
        """

        return self.ai_service.generate_structured(
            prompt,
            ResumeData,
        )

resume_parser_service = ResumeParserService()