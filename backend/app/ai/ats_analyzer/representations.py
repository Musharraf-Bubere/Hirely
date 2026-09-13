from app.ai.ats_analyzer.context import ATSContext
from app.ai.parsers.schemas import ResumeData


class ATSRepresentationBuilder:
    """
    Builds controlled text representations for semantic comparison.

    This component prepares resume and job information for embedding.
    It intentionally excludes direct contact information such as email
    and phone number.
    """

    def build_resume_text(
        self,
        resume: ResumeData,
    ) -> str:
        sections: list[str] = []

        if resume.name:
            sections.append(f"Candidate: {resume.name}")

        if resume.headline:
            sections.append(f"Headline: {resume.headline}")

        if resume.summary:
            sections.append(f"Summary: {resume.summary}")

        if resume.skills:
            skills = ", ".join(
                skill.strip()
                for skill in resume.skills
                if skill and skill.strip()
            )

            if skills:
                sections.append(f"Skills: {skills}")

        for experience in resume.experience:
            experience_parts = [
                f"Company: {experience.company}"
                if experience.company
                else None,
                f"Job Title: {experience.job_title}"
                if experience.job_title
                else None,
                f"Start Date: {experience.start_date}"
                if experience.start_date
                else None,
                f"End Date: {experience.end_date}"
                if experience.end_date
                else None,
                f"Description: {experience.description}"
                if experience.description
                else None,
            ]

            content = "\n".join(
                part
                for part in experience_parts
                if part
            )

            if content:
                sections.append(
                    f"Work Experience:\n{content}"
                )

        for project in resume.projects:
            project_parts = [
                f"Project: {project.name}"
                if project.name
                else None,
                f"Description: {project.description}"
                if project.description
                else None,
                (
                    "Technologies: "
                    + ", ".join(
                        technology.strip()
                        for technology in project.technologies
                        if technology and technology.strip()
                    )
                )
                if project.technologies
                else None,
            ]

            content = "\n".join(
                part
                for part in project_parts
                if part
            )

            if content:
                sections.append(
                    f"Project:\n{content}"
                )

        for education in resume.education:
            education_parts = [
                f"Institution: {education.institution}"
                if education.institution
                else None,
                f"Degree: {education.degree}"
                if education.degree
                else None,
                f"Field of Study: {education.field_of_study}"
                if education.field_of_study
                else None,
                f"Start Date: {education.start_date}"
                if education.start_date
                else None,
                f"End Date: {education.end_date}"
                if education.end_date
                else None,
            ]

            content = "\n".join(
                part
                for part in education_parts
                if part
            )

            if content:
                sections.append(
                    f"Education:\n{content}"
                )

        for certification in resume.certifications:
            certification_parts = [
                f"Certification: {certification.name}"
                if certification.name
                else None,
                f"Issuer: {certification.issuer}"
                if certification.issuer
                else None,
                f"Date: {certification.date}"
                if certification.date
                else None,
            ]

            content = "\n".join(
                part
                for part in certification_parts
                if part
            )

            if content:
                sections.append(
                    f"Certification:\n{content}"
                )

        return "\n\n".join(sections).strip()

    def build_job_text(
        self,
        context: ATSContext,
    ) -> str:
        job = context.job

        sections: list[str] = [
            f"Job Title: {job.title}",
            f"Job Description: {job.description}",
        ]

        if job.location:
            sections.append(
                f"Location: {job.location}"
            )

        if job.employment_type:
            sections.append(
                f"Employment Type: {job.employment_type}"
            )

        if job.experience_level:
            sections.append(
                f"Experience Level: {job.experience_level}"
            )

        if job.required_skills:
            sections.append(
                "Required Skills: "
                + ", ".join(job.required_skills)
            )

        if job.preferred_skills:
            sections.append(
                "Preferred Skills: "
                + ", ".join(job.preferred_skills)
            )

        return "\n".join(sections).strip()

    def build(
        self,
        context: ATSContext,
    ) -> tuple[str, str]:
        resume_text = self.build_resume_text(
            context.candidate.resume
        )

        job_text = self.build_job_text(
            context
        )

        if not resume_text:
            raise ValueError(
                "Resume does not contain enough information "
                "for semantic analysis."
            )

        if not job_text:
            raise ValueError(
                "Job does not contain enough information "
                "for semantic analysis."
            )

        return resume_text, job_text


ats_representation_builder = ATSRepresentationBuilder()