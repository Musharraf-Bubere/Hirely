from uuid import uuid4

from app.ai.parsers.schemas import ResumeData
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.user import User, UserRole
from app.services.resume import create_resume, parse_resume


class FakeResumeParserService:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.received_file_path = None

    def parse_file(self, file_path):
        self.received_file_path = file_path

        if self.error:
            raise self.error

        return self.result


def create_test_candidate(db):
    user = User(
        email=f"resume-parser-{uuid4()}@example.com",
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.CANDIDATE,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    candidate = Candidate(
        user_id=user.id,
        first_name="Test",
        last_name="Candidate",
        headline="Python Developer",
        bio="Resume parser service test candidate.",
        location="India",
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return user, candidate


def test_parse_resume_success():
    db = SessionLocal()

    user = None
    candidate = None
    resume = None

    try:
        user, candidate = create_test_candidate(db)

        resume = create_resume(
            db=db,
            candidate=candidate,
            original_filename="test_resume.pdf",
            file_path="test_data/test_resume.pdf",
        )

        resume_data = ResumeData(
            name="Test Candidate",
            email="test@example.com",
            skills=["Python", "SQL"],
        )

        parser = FakeResumeParserService(
            result=resume_data,
        )

        result = parse_resume(
            db=db,
            resume=resume,
            parser_service=parser,
        )

        assert parser.received_file_path == "test_data/test_resume.pdf"

        assert result.parsing_status == "COMPLETED"
        assert result.parsed_data == resume_data.model_dump()

        persisted_resume = (
            db.query(Resume)
            .filter(Resume.id == resume.id)
            .first()
        )

        assert persisted_resume is not None
        assert persisted_resume.parsing_status == "COMPLETED"
        assert persisted_resume.parsed_data == resume_data.model_dump()

    finally:
        if resume:
            db.delete(resume)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()


def test_parse_resume_failure_marks_resume_failed():
    db = SessionLocal()

    user = None
    candidate = None
    resume = None

    try:
        user, candidate = create_test_candidate(db)

        resume = create_resume(
            db=db,
            candidate=candidate,
            original_filename="test_resume.pdf",
            file_path="test_data/test_resume.pdf",
        )

        parser = FakeResumeParserService(
            error=RuntimeError("Parser failed"),
        )

        try:
            parse_resume(
                db=db,
                resume=resume,
                parser_service=parser,
            )
            assert False, "Expected parser error was not raised"

        except RuntimeError as exc:
            assert str(exc) == "Parser failed"

        db.refresh(resume)

        assert resume.parsing_status == "FAILED"

    finally:
        if resume:
            db.delete(resume)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()