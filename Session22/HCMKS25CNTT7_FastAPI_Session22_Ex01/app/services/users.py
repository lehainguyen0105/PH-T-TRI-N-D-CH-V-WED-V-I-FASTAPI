"""services/users.copy()"""

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core import security
from app.models.users import Users
from app.schemas.users import CreateUser, LoginUser


def create_auth(db: Session, data: CreateUser):
    """Đăng ký tài khoản"""

    exist_user = db.query(Users).filter(Users.username == data.username).first()
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username đã tồn tại"
        )
    try:
        hashed_password = security.hash_password(password=data.password)

        new_user = Users(
            username=data.username,
            password=hashed_password,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi cơ sở dữ liệu: {e}",
        ) from e


def authenticate_user(db: Session, data: LoginUser):
    """Đăng nhập"""

    user = db.query(Users).filter(Users.username == data.username).first()

    if not user or not security.verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên hoặc mật khẩu không đúng",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
