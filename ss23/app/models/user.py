from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Khóa ngoại: Liên kết tới bảng roles (Quan hệ N-1: Nhiều user có thể cùng 1 role)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)

    # Relationship: Quan hệ 2 chiều với Role
    # - Chiều xuôi:  user.role  → lấy object Role của user đó
    # - Chiều ngược: role.users → lấy danh sách tất cả User có role đó
    # back_populates="users" phải khớp với tên attribute trong class Role
    role = relationship("Role", back_populates="users")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

