import jwt

from app.core.config import settings
from app.core.security import create_access_token, decode_access_token


token = create_access_token(
    "12345678-1234-1234-1234-123456789012",
    "candidate",
)

# Valid token
payload = decode_access_token(token)

print("Valid token accepted:", payload["sub"] == "12345678-1234-1234-1234-123456789012")

# Tamper with the payload
parts = token.split(".")
tampered_token = parts[0] + "." + parts[1][:-1] + "X." + parts[2]

try:
    decode_access_token(tampered_token)
    print("ERROR: tampered token accepted")
except jwt.InvalidTokenError:
    print("Tampered token rejected: True")

# Completely invalid token
try:
    decode_access_token("this.is.not.a.valid.jwt")
    print("ERROR: invalid token accepted")
except jwt.InvalidTokenError:
    print("Invalid token rejected: True")