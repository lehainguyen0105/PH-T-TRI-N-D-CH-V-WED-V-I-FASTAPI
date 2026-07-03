from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date
from typing import List, Optional

app = FastAPI(version="1.0")

class CarrierStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"

class ShiftType(str, Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    NIGHT = "NIGHT"

class Carriers(BaseModel):
    code: str
    name: str = Field(..., min_length=3)
    max_weight_capacity: float = Field(..., gt=0)
    status: CarrierStatus

class CarrierResponse(BaseModel):
    id: int
    code: str
    name: str
    max_weight_capacity: float
    status: CarrierStatus

class ShipmentRequest(BaseModel):
    carrier_id: int
    order_reference: str = Field(..., min_length=1)
    total_weight: float = Field(..., gt=0)
    dispatch_date: date
    shift: ShiftType

class ShipmentResponse(BaseModel):
    id: int
    carrier_id: int
    order_reference: str
    total_weight: float
    dispatch_date: date
    shift: ShiftType

carriers = [
    {"id": 1, "code": "GHN", "name": "Giao Hang Nhanh", "max_weight_capacity": 5000.0, "status": CarrierStatus.ACTIVE},
    {"id": 2, "code": "GHTK", "name": "Giao Hang Tiet Kiem", "max_weight_capacity": 3000.0, "status": CarrierStatus.ACTIVE},
    {"id": 3, "code": "VTP", "name": "Viettel Post", "max_weight_capacity": 10000.0, "status": CarrierStatus.SUSPENDED}
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200.0,
        "dispatch_date": date(2026, 7, 1),
        "shift": ShiftType.MORNING
    }
]

@app.post("/carriers", response_model=CarrierResponse, status_code=status.HTTP_201_CREATED)
def create_carrier(carrier_data: Carriers):
    if any(c["code"] == carrier_data.code for c in carriers):
        raise HTTPException(status_code=400, detail="Carrier code already exists")
    new_id = max((c["id"] for c in carriers), default=0) + 1
    new_carrier = {"id": new_id, **carrier_data.model_dump()}
    carriers.append(new_carrier)
    return new_carrier

@app.get("/carriers", response_model=List[CarrierResponse])
def get_carriers(
    keyword: Optional[str] = None,
    status: Optional[CarrierStatus] = None,
    min_weight: Optional[float] = None
):
    new_carriers = carriers.copy()
    if keyword:
        new_carriers = [c for c in new_carriers if keyword.lower() in c["name"].lower() or keyword.lower() in c["code"].lower()]
    if status:
        new_carriers = [c for c in new_carriers if c["status"] == status]
    if min_weight is not None:
        new_carriers = [c for c in new_carriers if c["max_weight_capacity"] >= min_weight]
    return new_carriers

@app.get("/carriers/{carrier_id}", response_model=CarrierResponse)
def get_carrier_detail(carrier_id: int):
    carrier = next((c for c in carriers if c["id"] == carrier_id), None)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    return carrier

@app.put("/carriers/{carrier_id}", response_model=CarrierResponse)
def update_carrier(carrier_id: int, carrier_data: Carriers):
    carrier = next((c for c in carriers if c["id"] == carrier_id), None)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    if any(c["code"] == carrier_data.code and c["id"] != carrier_id for c in carriers):
        raise HTTPException(status_code=400, detail="Carrier code already exists on another carrier")
    carrier.update(carrier_data.model_dump())
    return carrier

@app.delete("/carriers/{carrier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_carrier(carrier_id: int):
    carrier = next((c for c in carriers if c["id"] == carrier_id), None)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    carriers.remove(carrier)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/shipments", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
def create_shipment(shipment_data: ShipmentRequest):
    carrier = next((c for c in carriers if c["id"] == shipment_data.carrier_id), None)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    if carrier["status"] != CarrierStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Carrier is not ACTIVE")
    if shipment_data.total_weight > carrier["max_weight_capacity"]:
        raise HTTPException(status_code=400, detail=f"Total weight exceeds carrier capacity. Max: {carrier['max_weight_capacity']}")
    is_duplicated = any(
        s["carrier_id"] == shipment_data.carrier_id and 
        s["dispatch_date"] == shipment_data.dispatch_date and 
        s["shift"] == shipment_data.shift 
        for s in shipments
    )
    if is_duplicated:
        raise HTTPException(status_code=400, detail="Carrier is already scheduled for this date and shift")
    new_shipment_id = max((s["id"] for s in shipments), default=0) + 1
    new_shipment = {
        "id": new_shipment_id,
        "carrier_id": shipment_data.carrier_id,
        "order_reference": shipment_data.order_reference,
        "total_weight": shipment_data.total_weight,
        "dispatch_date": shipment_data.dispatch_date,
        "shift": shipment_data.shift
    }
    shipments.append(new_shipment)
    return new_shipment

@app.get("/shipments", response_model=List[ShipmentResponse])
def get_all_shipments():
    return shipments