from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date
from typing import List, Optional

app = FastAPI(title="Co-working Space Booking System")

class DeskStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    MAINTENANCE = "MAINTENANCE"

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

class DeskCreateDTO(BaseModel):
    desk_number: str = Field(..., description="Mã số bàn làm việc không được trùng lặp")
    zone: str = Field(..., description="Khu vực vị trí bàn làm việc")
    price_per_day: float = Field(..., gt=0, description="Giá thuê mỗi ngày phải lớn hơn 0")
    status: DeskStatus = Field(..., description="Trạng thái bàn")

class DeskResponseDTO(BaseModel):
    id: int
    desk_number: str
    zone: str
    price_per_day: float
    status: DeskStatus

class BookingCreateDTO(BaseModel):
    desk_id: int
    customer_name: str = Field(..., min_length=1)
    booking_date: date
    payment_status: PaymentStatus

class BookingResponseDTO(BaseModel):
    id: int
    desk_id: int
    customer_name: str
    booking_date: date
    payment_status: PaymentStatus

desks = [
    {"id": 1, "desk_number": "DSK-A-01", "zone": "Zone A - Quiet Space", "price_per_day": 150000.0, "status": DeskStatus.AVAILABLE},
    {"id": 2, "desk_number": "DSK-B-02", "zone": "Zone B - Creative", "price_per_day": 200000.0, "status": DeskStatus.AVAILABLE},
    {"id": 3, "desk_number": "DSK-C-03", "zone": "Zone C - Panoramic", "price_per_day": 250000.0, "status": DeskStatus.MAINTENANCE}
]

bookings = [
    {
        "id": 1,
        "desk_id": 1,
        "customer_name": "Nguyen Van A",
        "booking_date": date(2026, 7, 1),
        "payment_status": PaymentStatus.PAID
    }
]

@app.post("/desks", response_model=DeskResponseDTO, status_code=status.HTTP_201_CREATED)
def create_desk(desk_data: DeskCreateDTO):
    if any(d["desk_number"] == desk_data.desk_number for d in desks):
        raise HTTPException(status_code=400, detail="Desk number already exists")
    
    new_id = max((d["id"] for d in desks), default=0) + 1
    new_desk = {"id": new_id, **desk_data.model_dump()}
    desks.append(new_desk)
    return new_desk

@app.get("/desks", response_model=List[DeskResponseDTO])
def get_all_desks(
    zone_keyword: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    status: Optional[DeskStatus] = Query(None)
):
    filtered_desks = desks
    
    if zone_keyword:
        zk_lower = zone_keyword.lower()
        filtered_desks = [d for d in filtered_desks if zk_lower in d["zone"].lower()]
        
    if max_price is not None:
        filtered_desks = [d for d in filtered_desks if d["price_per_day"] <= max_price]
        
    if status:
        filtered_desks = [d for d in filtered_desks if d["status"] == status]
        
    return filtered_desks

@app.get("/desks/{desk_id}", response_model=DeskResponseDTO)
def get_desk_detail(desk_id: int):
    desk = next((d for d in desks if d["id"] == desk_id), None)
    if not desk:
        raise HTTPException(status_code=404, detail="Desk not found")
    return desk

@app.put("/desks/{desk_id}", response_model=DeskResponseDTO)
def update_desk(desk_id: int, desk_data: DeskCreateDTO):
    desk = next((d for d in desks if d["id"] == desk_id), None)
    if not desk:
        raise HTTPException(status_code=404, detail="Desk not found")
        
    if any(d["desk_number"] == desk_data.desk_number and d["id"] != desk_id for d in desks):
        raise HTTPException(status_code=400, detail="Desk number already exists on another desk")
        
    desk.update(desk_data.model_dump())
    return desk

@app.delete("/desks/{desk_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_desk(desk_id: int):
    desk = next((d for d in desks if d["id"] == desk_id), None)
    if not desk:
        raise HTTPException(status_code=404, detail="Desk not found")
        
    desks.remove(desk)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/bookings", response_model=BookingResponseDTO, status_code=status.HTTP_201_CREATED)
def create_booking(booking_data: BookingCreateDTO):
    desk = next((d for d in desks if d["id"] == booking_data.desk_id), None)
    if not desk:
        raise HTTPException(status_code=404, detail="Desk not found")
        
    if desk["status"] != DeskStatus.AVAILABLE:
        raise HTTPException(status_code=400, detail="Desk is not AVAILABLE for booking")
        
    is_overbooking = any(
        b["desk_id"] == booking_data.desk_id and b["booking_date"] == booking_data.booking_date 
        for b in bookings
    )
    if is_overbooking:
        raise HTTPException(status_code=400, detail="This desk has already been booked for this date")
        
    new_booking_id = max((b["id"] for b in bookings), default=0) + 1
    new_booking = {
        "id": new_booking_id,
        "desk_id": booking_data.desk_id,
        "customer_name": booking_data.customer_name,
        "booking_date": booking_data.booking_date,
        "payment_status": booking_data.payment_status
    }
    bookings.append(new_booking)
    return new_booking

@app.get("/bookings", response_model=List[BookingResponseDTO])
def get_all_bookings():
    return bookings