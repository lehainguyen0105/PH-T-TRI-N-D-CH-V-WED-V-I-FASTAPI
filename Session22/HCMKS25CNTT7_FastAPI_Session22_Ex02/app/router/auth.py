from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.schemas.auth import (
    StaffLoginRequest,
    StaffRegisterRequest,
    StaffResponse,
    TokenResponse,
)
from app.services import auth_service

DbDep = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/medical", tags=["Medical Authentication"])


@router.post(
    "/register",
    response_model=StaffResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản Bác sĩ / Dược sĩ",
)
def register(data: StaffRegisterRequest, db: DbDep):
    return auth_service.register_staff(db=db, data=data)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Đăng nhập và nhận JWT 20 phút kèm Role Claim",
)
def login(data: StaffLoginRequest, db: DbDep):
    staff = auth_service.authenticate_staff(db=db, data=data)
    token = security.create_access_token(subject=staff.username, role=staff.role)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
