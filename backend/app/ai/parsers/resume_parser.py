from pathlib import Path

from app.ai.loaders.resume_loader import ResumeLoader
from app.ai.parsers.schemas import ResumeData
from app.ai.services.gemini_service import gemini_service


class ResumeParserService:
    def __init__(
        self, 
        ai_service=gemini_service,
        resume_loader=None,
    ):
        
        self.ai_service = ai_service
        self.resume_loader = resume_loader or ResumeLoader()

    def parse(self, resume_text: str) -> ResumeData:
        prompt = f"""
        Extract structured candidate information from the resume below.

        Follow these rules carefully:

        - Extract only information explicitly present in the resume.
        - Do not invent, assume, or infer missing information.
        - If a field is not present, return null for optional scalar fields.
        - If a section is not present, return an empty list for that section.
        - Preserve the meaning of the candidate's original information.
        - Keep skills as individual skill names or technologies.
        - Put employment or professional work history in experience.
        - Put academic, personal, or portfolio projects in projects.
        - Put formal certifications in certifications.
        - Put academic qualifications in education.
        - Use "institution" for the education institution field.
        - Keep dates as they appear in the resume when possible.
        - Do not convert projects into employment experience.
        - Do not convert skills into experience.
        - Do not create a headline unless the resume explicitly contains one.

        Resume:
        {resume_text}
        """

        return self.ai_service.generate_structured(
            prompt,
            ResumeData,
        )

    def parse_file(self, file_path: str | Path) -> ResumeData:
        resume_text = self.resume_loader.load_text(file_path)

        return self.parse(resume_text)
    

resume_parser_service = ResumeParserService()