from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Clinic, Doctor, License
from schemas import ClinicCreate, DoctorUpdate
from sqlalchemy.exc import SQLAlchemyError

def create_clinic(db: Session, data: ClinicCreate):
    try:
        new_clinic = Clinic(**data.model_dump())
        db.add(new_clinic)
        db.commit()
        db.refresh(new_clinic)
        return new_clinic
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi cơ sở dữ liệu khi tạo mới phòng khám"
        )

def get_clinic_detail(db: Session, clinic_id: int):
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if clinic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phòng khám không tồn tại"
        )
    return clinic

def patch_doctor(db: Session, doctor_id: int, data: DoctorUpdate):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bác sĩ không tồn tại"
            )
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(doctor, key, value)
            
        db.commit()
        db.refresh(doctor)
        return doctor
    except HTTPException as he:
        raise he
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi cơ sở dữ liệu khi cập nhật thông tin bác sĩ"
        )

def delete_license(db: Session, license_id: int):
    try:
        license_obj = db.query(License).filter(License.id == license_id).first()
        if license_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chứng chỉ hành nghề không tồn tại"
            )
        
        db.delete(license_obj)
        db.commit()
        return license_obj
    except HTTPException as he:
        raise he
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi cơ sở dữ liệu khi xóa chứng chỉ hành nghề"
        )