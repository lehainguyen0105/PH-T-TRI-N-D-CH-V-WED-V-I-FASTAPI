from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Clinic(Base):
    __tablename__ = "clinics"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    clinic_name = Column(String(100), nullable=False)
    specialty = Column(String(100), nullable=False)

    doctors = relationship("Doctor", back_populates="clinic")

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    doctor_code = Column(String(100), unique=True, nullable=False)
    salary = Column(Float, nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)

    clinic = relationship("Clinic", back_populates="doctors")
    license = relationship("License", back_populates="doctor", uselist=False)

class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    license_number = Column(String(100), unique=True, nullable=False)
    issue_by = Column(String(100), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), unique=True, nullable=False)

    doctor = relationship("Doctor", back_populates="license")