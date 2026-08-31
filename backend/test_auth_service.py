from app.core.security import verify_password
from app.db.session import SessionLocal
from app.models import User
from app.schemas.auth import RegisterRequest
from app.services.auth import authenticate_user, register_user


db = SessionLocal()

test_email = "auth-service-test@example.com"

try:
    # Clean up any previous test data
    existing_user = (
        db.query(User)
        .filter(User.email == test_email)
        .first()
    )

    if existing_user:
        db.delete(existing_user)
        db.commit()

    # -------------------------
    # Registration
    # -------------------------

    data = RegisterRequest(
        email=test_email,
        password="secret123",
        role="candidate",
    )

    user = register_user(db, data)

    print("User ID:", user.id)
    print("Email:", user.email)
    print("Role:", user.role)
    print("Password is hashed:", user.password_hash != "secret123")
    print(
        "Stored password verifies:",
        verify_password("secret123", user.password_hash),
    )

    # -------------------------
    # Successful authentication
    # -------------------------

    authenticated_user = authenticate_user(
        db,
        test_email,
        "secret123",
    )

    print(
        "Correct credentials:",
        authenticated_user is not None,
    )

    # -------------------------
    # Wrong password
    # -------------------------

    wrong_password_user = authenticate_user(
        db,
        test_email,
        "wrong-password",
    )

    print(
        "Wrong password rejected:",
        wrong_password_user is None,
    )

    # -------------------------
    # Nonexistent user
    # -------------------------

    nonexistent_user = authenticate_user(
        db,
        "does-not-exist@example.com",
        "secret123",
    )

    print(
        "Unknown user rejected:",
        nonexistent_user is None,
    )

finally:
    # -------------------------
    # Cleanup
    # -------------------------

    test_user = (
        db.query(User)
        .filter(User.email == test_email)
        .first()
    )

    if test_user:
        db.delete(test_user)
        db.commit()

    db.close()

print("Test data cleaned up.")