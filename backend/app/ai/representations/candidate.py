from pydantic import BaseModel

from app.ai.parsers.schemas import ResumeData


class CandidateRepresentation(BaseModel):
    profile_text: str


class CandidateRepresentationBuilder:
    def build(self, resume_data: ResumeData) -> CandidateRepresentation:
        sections: list[str] = []

        sections.append("Candidate Profile")

        if resume_data.location:
            sections.append(
                f"Location:\n{resume_data.location}"
            )

        if resume_data.headline:
            sections.append(
                f"Headline:\n{resume_data.headline}"
            )

        if resume_data.summary:
            sections.append(
                f"Summary:\n{resume_data.summary}"
            )

        if resume_data.skills:
            skills = ", ".join(resume_data.skills)
            sections.append(
                f"Skills:\n{skills}"
            )

        experience_entries: list[str] = []

        for experience in resume_data.experience:
            entry: list[str] = []

            if experience.job_title and experience.company:
                entry.append(
                    f"{experience.job_title} at {experience.company}"
                )
            elif experience.job_title:
                entry.append(experience.job_title)
            elif experience.company:
                entry.append(experience.company)

            if experience.start_date or experience.end_date:
                start = experience.start_date or ""
                end = experience.end_date or ""
                entry.append(f"{start} - {end}".strip(" -"))

            if experience.description:
                entry.append(experience.description)

            if entry:
                experience_entries.append("\n".join(entry))

        if experience_entries:
            sections.append(
                "Professional Experience:\n"
                + "\n\n".join(experience_entries)
            )

        project_entries: list[str] = []

        for project in resume_data.projects:
            entry: list[str] = []

            if project.name:
                entry.append(project.name)

            if project.description:
                entry.append(project.description)

            if project.technologies:
                technologies = ", ".join(project.technologies)
                entry.append(f"Technologies: {technologies}")

            if entry:
                project_entries.append("\n".join(entry))

        if project_entries:
            sections.append(
                "Projects:\n"
                + "\n\n".join(project_entries)
            )

        education_entries: list[str] = []

        for education in resume_data.education:
            entry: list[str] = []

            if education.degree:
                entry.append(education.degree)

            if education.institution:
                entry.append(education.institution)

            if education.field_of_study:
                entry.append(
                    f"Field of Study: {education.field_of_study}"
                )

            if education.start_date or education.end_date:
                start = education.start_date or ""
                end = education.end_date or ""
                entry.append(f"{start} - {end}".strip(" -"))

            if entry:
                education_entries.append("\n".join(entry))

        if education_entries:
            sections.append(
                "Education:\n"
                + "\n\n".join(education_entries)
            )

        certification_entries: list[str] = []

        for certification in resume_data.certifications:
            entry: list[str] = []

            if certification.name:
                entry.append(certification.name)

            if certification.issuer:
                entry.append(f"Issuer: {certification.issuer}")

            if certification.date:
                entry.append(f"Date: {certification.date}")

            if entry:
                certification_entries.append("\n".join(entry))

        if certification_entries:
            sections.append(
                "Certifications:\n"
                + "\n\n".join(certification_entries)
            )

        profile_text = "\n\n".join(sections)

        return CandidateRepresentation(
            profile_text=profile_text
        )


candidate_representation_builder = CandidateRepresentationBuilder()