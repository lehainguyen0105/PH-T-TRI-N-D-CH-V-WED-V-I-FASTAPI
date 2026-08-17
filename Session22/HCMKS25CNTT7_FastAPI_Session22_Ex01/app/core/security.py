"""core/security.py"""

import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi.security import HTTPBearer

auth_scheme = HTTPBearer()

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "khoa_bi_mat_mac_dinh_tam_thoi")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str, cost_factor: int = 12) -> str:
    """Băm mật khẩu"""

    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=cost_factor)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)

    return hashed_bytes.decode("utf-8")


def verify_password(password_bytes: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu có khớp với trong db ko"""
    password_bytes = password_bytes.encode("utf-8")
    hashed_password = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_password)


def create_access_token(data: dict) -> str:
    """Tạo Access Token (PWT) dựa trên payload(data)"""
    to_encode = data.copy()

    # Thời gian hết hạn
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Ký và tạo token
    encoding_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoding_jwt


def decode_access_token(token: str):
    """Giải mã và kiểm tra tính hợp lệ của token"""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
