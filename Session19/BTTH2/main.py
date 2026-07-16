from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import hospital_services
import schemas

app = FastAPI(
    title="HỆ THỐNG QUẢN LÝ Y TẾ"
)

Base.metadata.create_all(bind=engine)

@app.post(
    "/clinics", 
    response_model=schemas.ClinicDetailResponse, 
    status_code=status.HTTP_201_CREATED, 
    tags=["Clinics"]
)
def create_clinic(data: schemas.ClinicCreate, db: Session = Depends(get_db)):
    result = hospital_services.create_clinic(db, data)
    return result

@app.get(
    "/clinics/{clinic_id}", 
    response_model=schemas.ClinicDetailResponse, 
    status_code=status.HTTP_200_OK, 
    tags=["Clinics"]
)
def get_clinic_detail(clinic_id: int, db: Session = Depends(get_db)):
    result = hospital_services.get_clinic_detail(db, clinic_id)
    return result

@app.patch(
    "/doctors/{doctor_id}", 
    response_model=schemas.DoctorResponse, 
    status_code=status.HTTP_200_OK, 
    tags=["Doctors"]
)
def patch_doctor(doctor_id: int, data: schemas.DoctorUpdate, db: Session = Depends(get_db)):
    result = hospital_services.patch_doctor(db, doctor_id, data)
    return result

@app.delete(
    "/licenses/{license_id}", 
    status_code=status.HTTP_200_OK, 
    tags=["Licenses"]
)
def delete_license(license_id: int, db: Session = Depends(get_db)):
    hospital_services.delete_license(db, license_id)
    return {
        "message": "Xóa chứng chỉ hành nghề thành công"
    }