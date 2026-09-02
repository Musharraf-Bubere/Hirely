from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.models.company import Company
from app.models.recruiter import Recruiter
from app.models.user import User


def test_recruiter_company_relationship_persists():
    db = SessionLocal()

    user = None
    company = None
    recruiter = None

    try:
        # ---------------------------------------------------------
        # Create User
        # ---------------------------------------------------------
        user = User(
            email="company-test@example.com",
            password_hash="temporary-test-hash",
            role="RECRUITER",
        )

        db.add(user)

        # Flush so the User UUID is generated.
        db.flush()

        print("User ID:", user.id)

        # ---------------------------------------------------------
        # Create Company
        # ---------------------------------------------------------
        company = Company(
            name="Hirely Test Company",
            description="Temporary database relationship test",
            website="https://example.com",
            industry="Technology",
            location="India",
        )

        db.add(company)

        # Flush so the Company UUID is generated.
        db.flush()

        print("Company ID:", company.id)

        # ---------------------------------------------------------
        # Create Recruiter using the real User ID
        # ---------------------------------------------------------
        recruiter = Recruiter(
            user_id=user.id,
            first_name="Test",
            last_name="Recruiter",
            job_title="Talent Acquisition",
            location="India",
        )

        # Establish ORM relationship with Company.
        recruiter.company = company

        db.add(recruiter)

        # ---------------------------------------------------------
        # Commit all changes
        # ---------------------------------------------------------
        db.commit()

        print("Recruiter ID:", recruiter.id)
        print("Recruiter company:", recruiter.company.name)
        print("Company recruiters:", len(company.recruiters))

        # ---------------------------------------------------------
        # Verify relationship before refresh
        # ---------------------------------------------------------
        assert recruiter.company is not None
        assert recruiter.company.id == company.id
        assert recruiter.company.name == "Hirely Test Company"

        assert len(company.recruiters) == 1
        assert company.recruiters[0].id == recruiter.id

        # ---------------------------------------------------------
        # Refresh from database
        # ---------------------------------------------------------
        db.refresh(recruiter)

        print(
            "Persisted recruiter company:",
            recruiter.company.name,
        )

        # ---------------------------------------------------------
        # Verify relationship after database refresh
        # ---------------------------------------------------------
        assert recruiter.company is not None
        assert recruiter.company.id == company.id
        assert recruiter.company.name == "Hirely Test Company"

        print("Company-recruiter relationship test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if recruiter:
            db.delete(recruiter)

        if company:
            db.delete(company)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Test data cleaned up.")