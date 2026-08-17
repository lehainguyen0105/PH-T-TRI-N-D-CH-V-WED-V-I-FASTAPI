from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Dict, List, Optional
import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

# auto_error=False để kiểm soát phản hồi lỗi 401 tùy chỉnh
auth_scheme = HTTPBearer(auto_error=False)


def hash_password(plain_password: str) -> str:
    """Băm mật khẩu bằng bcrypt có salt ngẫu nhiên."""
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Xác thực mật khẩu với chuỗi hash trong DB."""
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(subject: str, role: str) -> str:
    """
    Sinh JWT Access Token:
    - sub: định danh
    - role: doctor/pharmacist
    - iat: thời gian tạo
    - exp: thời gian hết hạn (20 phút)
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": subject,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    token = jwt.encode(
        payload, settings.MEDCARE_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    """Giải mã và kiểm tra tính toàn vẹn của token."""
    try:
        payload = jwt.decode(
            token,
            settings.MEDCARE_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc chữ ký bị giả mạo",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_claims(
    credentials: Annotated[
        Optional[HTTPAuthorizationCredentials], Depends(auth_scheme)
    ],
) -> Dict[str, Any]:
    """Dependency lấy thông tin Claims từ Header Authorization."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thiếu header Authorization",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return decode_access_token(credentials.credentials)


class RoleChecker:
    """Dependency kiểm tra quyền hạn (Role-Based Access Control)."""

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        claims: Annotated[Dict[str, Any], Depends(get_current_user_claims)],
    ) -> Dict[str, Any]:
        user_role = claims.get("role")
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Không đủ quyền hạn truy cập tài nguyên này",
            )
        return claims
