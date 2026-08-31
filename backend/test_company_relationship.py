from app.db.session import SessionLocal
from app.models.user import User
from app.models.candidate import Candidate
from app.models.company import Company
from app.models.recruiter import Recruiter


db = SessionLocal()

try:
    # 1. Create User
    user = User(
        email="company-test@example.com",
        password_hash="temporary-test-hash",
        role="RECRUITER",
    )

    db.add(user)

    # Flush only the User so its UUID is generated.
    db.flush()

    print("User ID:", user.id)

    # 2. Create Company
    company = Company(
        name="Hirely Test Company",
        description="Temporary database relationship test",
        website="https://example.com",
        industry="Technology",
        location="India",
    )

    db.add(company)

    # Flush Company so its UUID is generated.
    db.flush()

    print("Company ID:", company.id)

    # 3. Create Recruiter using the real User ID
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

    # Commit all changes.
    db.commit()

    print("Recruiter ID:", recruiter.id)
    print("Recruiter company:", recruiter.company.name)
    print("Company recruiters:", len(company.recruiters))

    # 4. Refresh from database
    db.refresh(recruiter)

    print("Persisted recruiter company:", recruiter.company.name)

    # 5. Cleanup
    db.delete(recruiter)
    db.flush()

    db.delete(company)
    db.flush()

    db.delete(user)

    db.commit()

    print("Test data cleaned up.")

except Exception:
    db.rollback()
    raise

finally:
    db.close()