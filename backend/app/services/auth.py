from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.candidate import Candidate
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest


def register_user(
    db: Session,
    data: RegisterRequest,
) -> User:
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise ValueError("Email already registered")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
    )

    db.add(user)
    db.flush()

    if data.role == UserRole.CANDIDATE:
        candidate = Candidate(
            user_id=user.id,
            first_name=data.first_name,
            last_name=data.last_name,
        )

        db.add(candidate)

    elif data.role == UserRole.RECRUITER:
        recruiter = Recruiter(
            user_id=user.id,
            first_name=data.first_name,
            last_name=data.last_name,
        )

        db.add(recruiter)

    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user