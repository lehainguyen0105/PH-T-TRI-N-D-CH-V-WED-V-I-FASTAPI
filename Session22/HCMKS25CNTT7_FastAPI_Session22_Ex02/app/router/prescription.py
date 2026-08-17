from typing import Annotated, Any, Dict, List
import uuid
from fastapi import APIRouter, Depends, status

from app.core.security import RoleChecker
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse

router = APIRouter(prefix="/prescriptions", tags=["E-Prescriptions"])

# Phân quyền: Tạo đơn chỉ cho doctor, Xem đơn cho cả doctor và pharmacist
RequireDoctor = Annotated[
    Dict[str, Any], Depends(RoleChecker(allowed_roles=["doctor"]))
]
RequireMedicalStaff = Annotated[
    Dict[str, Any],
    Depends(RoleChecker(allowed_roles=["doctor", "pharmacist"])),
]

# Database RAM giả lập lưu đơn thuốc
PRESCRIPTIONS_STORE: List[dict] = []


@router.post(
    "",
    response_model=PrescriptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ký và phát hành đơn thuốc điện tử (Chỉ Bác sĩ)",
)
def create_prescription(data: PrescriptionCreate, claims: RequireDoctor):
    prescription_record = {
        "prescription_id": f"RX-{uuid.uuid4().hex[:8].upper()}",
        "patient_id": data.patient_id,
        "patient_name": data.patient_name,
        "diagnosis": data.diagnosis,
        "medicines": [med.model_dump() for med in data.medicines],
        "signed_by_doctor": claims.get("sub"),
        "status": "ISSUED",
    }
    PRESCRIPTIONS_STORE.append(prescription_record)
    return prescription_record


@router.get(
    "/view",
    response_model=List[PrescriptionResponse],
    status_code=status.HTTP_200_OK,
    summary="Xem danh sách đơn thuốc để xuất dược phẩm (Bác sĩ & Dược sĩ)",
)
def view_prescriptions(claims: RequireMedicalStaff):
    return PRESCRIPTIONS_STORE
