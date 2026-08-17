from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String
from app.db.session import Base


class MedicalStaff(Base):
    __tablename__ = "medical_staffs"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # "doctor" hoặc "pharmacist"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
