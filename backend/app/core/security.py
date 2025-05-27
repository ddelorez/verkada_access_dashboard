from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
# IMPORTANT: This is a placeholder secret key.
# In a production environment, use a strong, randomly generated key
# and load it from environment variables.
SECRET_KEY = "your-super-secret-key-please-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Access token validity period

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.

    Args:
        plain_password: The plain text password.
        hashed_password: The hashed password from the database.

    Returns:
        True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain password.

    Args:
        password: The plain text password.

    Returns:
        The hashed password.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a new JWT access token.

    Args:
        data: The data to encode in the token (e.g., username).
        expires_delta: Optional timedelta for token expiry.
                       Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        The encoded JWT access token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodes a JWT access token.

    Args:
        token: The JWT token string.

    Returns:
        The decoded token payload as a dictionary if valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None