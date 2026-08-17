"""router/auth.py"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core import security
from app.db.database import get_db
from app.schemas.users import CreateUser, LoginUser, UserResponse
from app.services import users

router = APIRouter(prefix="/api", tags=["Authentication"])

auth_scheme = HTTPBearer(auto_error=False)

# Tạo Type Alias tái sử dụng (giúp code cực kỳ gọn và sạch)
DbDep = Annotated[Session, Depends(get_db)]
AuthDep = Annotated[HTTPAuthorizationCredentials | None, Depends(auth_scheme)]


@router.get(path="/")
def test_url():
    return "Kết nối thành công"


@router.post(
    path="/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_users(data: CreateUser, db: DbDep):
    """Tạo users"""
    result = users.create_auth(db=db, data=data)

    return result


@router.post(path="/login", status_code=status.HTTP_200_OK)
def login_users(data: LoginUser, db: DbDep):
    """Đăng nhập"""

    user = users.authenticate_user(db=db, data=data)

    access_token = security.create_access_token(
        data={"sub": user.username, "id": user.id}
    )

    return {
        "message": "Đăng nhập thành công",
        "access_token": access_token,
        "token_type": "bearer",
        "data": {
            "id": user.id,
            "username": user.username,
            "is_active": user.is_active,
            "created_at": user.created_at,
        },
    }


@router.get(path="/profile", status_code=status.HTTP_200_OK)
def check_token(credentials: AuthDep):
    """Kiểm tra token"""

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vui lòng cung cấp token đăng nhập",
        )

    token = credentials.credentials
    decoded = security.decode_access_token(token)
    if not decoded:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
        )

    return {"message": f"Welcome, {decoded.get('sub')}!"}
