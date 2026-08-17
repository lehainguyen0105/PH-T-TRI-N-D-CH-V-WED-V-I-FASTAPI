from typing import List
from pydantic import BaseModel


class MedicineItem(BaseModel):
    name: str
    dosage: str
    quantity: int


class PrescriptionCreate(BaseModel):
    patient_id: str
    patient_name: str
    diagnosis: str
    medicines: List[MedicineItem]


class PrescriptionResponse(BaseModel):
    prescription_id: str
    patient_id: str
    patient_name: str
    diagnosis: str
    medicines: List[MedicineItem]
    signed_by_doctor: str
    status: str
