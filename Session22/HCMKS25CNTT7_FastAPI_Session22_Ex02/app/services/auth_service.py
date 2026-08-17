from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core import security
from app.models.medical_staff import MedicalStaff
from app.schemas.auth import StaffLoginRequest, StaffRegisterRequest


def register_staff(db: Session, data: StaffRegisterRequest) -> MedicalStaff:
    existing_user = (
        db.query(MedicalStaff).filter(MedicalStaff.username == data.username).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên tài khoản đã tồn tại trong hệ thống MedCare",
        )

    hashed_pw = security.hash_password(data.password)
    new_staff = MedicalStaff(
        username=data.username,
        hashed_password=hashed_pw,
        role=data.role.value,
    )
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    return new_staff


def authenticate_staff(db: Session, data: StaffLoginRequest) -> MedicalStaff:
    staff = (
        db.query(MedicalStaff).filter(MedicalStaff.username == data.username).first()
    )

    # Báo lỗi mập mờ, không chỉ đích danh sai mật khẩu hay sai username
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Thông tin đăng nhập không chính xác",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not staff:
        raise auth_exception

    if not security.verify_password(data.password, staff.hashed_password):
        raise auth_exception

    return staff
