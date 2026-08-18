from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.db.database import get_db
from app.services import user_service
from app.core.security import create_access_token

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint Đăng ký tài khoản:
    - Nhận vào thông tin UserCreate (email, password).
    - Gọi tầng service để xử lý logic lưu vào database.
    - Trả về thông tin UserResponse (chứa id, email, is_active, created_at) thay vì toàn bộ Object.
    """
    new_user = user_service.create_user(db=db, user_data=user_data)
    return new_user

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint Đăng nhập:
    - Nhận vào thông tin UserLogin (email, password).
    - Gọi tầng service để xác thực.
    - Tạo và trả về JWT Access Token cùng thông tin user.
    """
    user = user_service.authenticate_user(db=db, user_data=user_data)

    # Lấy tên role từ object relationship (user.role là object Role, user.role.name là chuỗi)
    role_name = user.role.name if user.role else None

    # Tạo JWT Access Token, nhét role_name vào payload để dùng cho Authorization
    access_token = create_access_token(data={"sub": user.email, "id": user.id, "role": role_name})

    return {
        "message": "Đăng nhập thành công",
        "access_token": access_token,
        "token_type": "bearer",
        "data": {
            "id": user.id,
            "email": user.email,
            "role": role_name,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
    }
