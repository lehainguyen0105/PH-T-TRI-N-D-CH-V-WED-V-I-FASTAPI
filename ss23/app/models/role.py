from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Role(Base):
    """
    Bảng lưu các vai trò (quyền) trong hệ thống.
    Ví dụ: user, admin, merchant, moderator,...
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)  # VD: "admin", "user"
    description = Column(String(255), nullable=True)                    # Mô tả quyền hạn

    # Quan hệ ngược lại (chiều ngược): 1 Role có thể có nhiều User
    # back_populates="role" phải khớp với tên attribute trong class User
    users = relationship("User", back_populates="role")

