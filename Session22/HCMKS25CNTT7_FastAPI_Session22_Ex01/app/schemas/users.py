"""schemas/users.py"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """Lớp cơ bản"""

    username: str
    password: str


class CreateUser(UserBase):
    """Lớp tạo tk"""


class LoginUser(UserBase):
    """Lớp đăng nhập"""


class UserResponse(BaseModel):
    """Lớp trả về"""

    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
