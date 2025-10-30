from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def sign_jwt(user_id: int) -> str:
    """Generate JWT token for user authentication."""
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_jwt(token: str) -> dict | None:
    """Decode and validate JWT token."""
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain, hashed)
