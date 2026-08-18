from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.core.config import settings

# Sử dụng HTTPBearer để lấy token từ header
reusable_oauth2 = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(reusable_oauth2),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency cốt lõi: Giải mã JWT từ Header, kiểm tra tính toàn vẹn,
    và truy vấn thông tin User từ cơ sở dữ liệu.
    """
    # Tự động lấy chuỗi Token nguyên bản
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin đăng nhập!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Bước 1: Giải mã Token bằng khóa bí mật
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Trong hệ thống hiện tại, "sub" lưu email
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise credentials_exception

    # Bước 2: Truy vấn thông tin người dùng từ DB thông qua SQLAlchemy ORM
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại trên hệ thống!"
        )

    # Bước 3: Kiểm tra xem tài khoản có đang bị khóa hay không
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản này đã bị tạm khóa!"
        )

    # Trả về đối tượng người dùng hoàn chỉnh cho endpoint kế tiếp
    return user


class RoleChecker:
    """
    Class Dependency dùng để phân quyền theo vai trò (Role-Based Access Control).
    Nhận vào một danh sách các role được phép truy cập.

    Cách dùng trong endpoint:
        Depends(RoleChecker(["admin"]))           # Chỉ admin
        Depends(RoleChecker(["admin", "manager"])) # Admin hoặc Manager
    """

    def __init__(self, allowed_roles: list[str]):
        # Lưu lại danh sách role được phép khi khởi tạo
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        # Lấy tên role từ relationship object (user.role là object Role)
        user_role_name = current_user.role.name if current_user.role else None

        # Kiểm tra role của user có nằm trong danh sách được phép không
        if user_role_name not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Quyền truy cập bị từ chối! Yêu cầu một trong các quyền: {self.allowed_roles}"
            )
        return current_user
