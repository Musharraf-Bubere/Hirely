import jwt

from app.core.security import create_access_token, decode_access_token


def test_jwt_valid_tampered_and_invalid_tokens():
    token = create_access_token(
        "12345678-1234-1234-1234-123456789012",
        "candidate",
    )

    # ---------------------------------------------------------
    # Valid token
    # Expected: token is successfully decoded
    # ---------------------------------------------------------
    payload = decode_access_token(token)

    assert payload["sub"] == "12345678-1234-1234-1234-123456789012"

    # ---------------------------------------------------------
    # Tamper with the payload
    # Expected: tampered token is rejected
    # ---------------------------------------------------------
    parts = token.split(".")
    tampered_token = parts[0] + "." + parts[1][:-1] + "X." + parts[2]

    try:
        decode_access_token(tampered_token)
        assert False, "Tampered token was accepted"
    except jwt.InvalidTokenError:
        pass

    # ---------------------------------------------------------
    # Completely invalid token
    # Expected: invalid token is rejected
    # ---------------------------------------------------------
    try:
        decode_access_token("this.is.not.a.valid.jwt")
        assert False, "Invalid token was accepted"
    except jwt.InvalidTokenError:
        pass