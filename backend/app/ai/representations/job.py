from pydantic import BaseModel


class JobRepresentation(BaseModel):
    job_text: str


class JobRepresentationBuilder:
    def build(
        self,
        title: str,
        description: str,
        location: str | None = None,
        employment_type: str | None = None,
        experience_level: str | None = None,
        required_skills: list[str] | None = None,
        preferred_skills: list[str] | None = None,
    ) -> JobRepresentation:
        sections: list[str] = []

        sections.append("Job Profile")

        if title:
            sections.append(
                f"Title:\n{title}"
            )

        if description:
            sections.append(
                f"Description:\n{description}"
            )

        if location:
            sections.append(
                f"Location:\n{location}"
            )

        if employment_type:
            sections.append(
                f"Employment Type:\n{employment_type}"
            )

        if experience_level:
            sections.append(
                f"Experience Level:\n{experience_level}"
            )

        if required_skills:
            sections.append(
                "Required Skills:\n"
                + ", ".join(required_skills)
            )

        if preferred_skills:
            sections.append(
                "Preferred Skills:\n"
                + ", ".join(preferred_skills)
            )

        job_text = "\n\n".join(sections)

        return JobRepresentation(
            job_text=job_text
        )


job_representation_builder = JobRepresentationBuilder()