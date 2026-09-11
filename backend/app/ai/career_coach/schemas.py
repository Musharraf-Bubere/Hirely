from pydantic import BaseModel, Field, field_validator


class CareerCoachRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=4000,
        description="Career-related question from the candidate.",
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty.")

        return value


class CareerCoachResponse(BaseModel):
    answer: str
    recommendations: list[str]
    skills_to_improve: list[str]
    next_steps: list[str]