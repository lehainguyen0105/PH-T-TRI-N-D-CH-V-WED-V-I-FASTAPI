from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict


class MedicalRole(str, Enum):
    DOCTOR = "doctor"
    PHARMACIST = "pharmacist"


class StaffRegisterRequest(BaseModel):
    username: str
    password: str
    role: MedicalRole


class StaffLoginRequest(BaseModel):
    username: str
    password: str


class StaffResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: MedicalRole
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
