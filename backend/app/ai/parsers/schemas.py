from pydantic import BaseModel


class WorkExperience(BaseModel):
    company: str | None = None
    job_title: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None


class Education(BaseModel):
    instituition: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class ResumeData(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None

    headline: str | None = None
    summary: str | None = None

    skills: list[str] = []

    experience: list[WorkExperience] = []
    education: list[Education] = []