from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date
from typing import List, Optional
import re

app = FastAPI(title="IT Asset Management System")

class AssetStatus(str, Enum):
    READY = "READY"
    ALLOCATED = "ALLOCATED"
    REPAIRING = "REPAIRING"
    SCRAPPED = "SCRAPPED"

class AssetCreateDTO(BaseModel):
    serial_number: str = Field(..., description="Mã serial duy nhất của thiết bị")
    model: str = Field(..., min_length=2, max_length=255, description="Tên model thiết bị")
    stock_available: int = Field(..., ge=0, description="Số lượng tồn kho khả dụng")
    status: AssetStatus = Field(..., description="Trạng thái thiết bị")

class AssetResponseDTO(BaseModel):
    id: int
    serial_number: str
    model: str
    stock_available: int
    status: AssetStatus

class AllocationCreateDTO(BaseModel):
    asset_id: int
    employee_email: str  
    allocated_quantity: int = Field(..., gt=0, description="Số lượng mượn phải lớn hơn 0")
    start_date: date
    duration_months: int = Field(..., ge=1, le=12, description="Thời gian mượn từ 1-12 tháng")

class AllocationResponseDTO(BaseModel):
    id: int
    asset_id: int
    employee_email: str
    allocated_quantity: int
    start_date: date
    duration_months: int

assets = [
    {"id": 1, "serial_number": "SN-MAC-01", "model": "MacBook Pro M3", "stock_available": 5, "status": AssetStatus.READY},
    {"id": 2, "serial_number": "SN-DELL-02", "model": "Dell UltraSharp 27", "stock_available": 10, "status": AssetStatus.READY},
    {"id": 3, "serial_number": "SN-THINK-03", "model": "ThinkPad X1 Carbon", "stock_available": 0, "status": AssetStatus.REPAIRING}
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": date(2026, 7, 1),
        "duration_months": 12
    }
]

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

@app.post("/assets", response_model=AssetResponseDTO, status_code=201)
def create_asset(asset_data: AssetCreateDTO):
    if any(a["serial_number"] == asset_data.serial_number for a in assets):
        raise HTTPException(status_code=400, detail="Serial number already exists")
        
    new_id = max((a["id"] for a in assets), default=0) + 1
    new_asset = {"id": new_id, **asset_data.model_dump()}
    assets.append(new_asset)
    return new_asset

@app.get("/assets", response_model=List[AssetResponseDTO])
def get_all_assets(
    keyword: Optional[str] = Query(None),
    status: Optional[AssetStatus] = Query(None),
    min_stock: Optional[int] = Query(None, ge=0)
):
    filtered_assets = assets
    
    if keyword:
        keyword_lower = keyword.lower()
        filtered_assets = [
            a for a in filtered_assets 
            if keyword_lower in a["serial_number"].lower() or keyword_lower in a["model"].lower()
        ]
        
    if status:
        filtered_assets = [a for a in filtered_assets if a["status"] == status]
        
    if min_stock is not None:
        filtered_assets = [a for a in filtered_assets if a["stock_available"] >= min_stock]
        
    return filtered_assets

@app.get("/assets/{asset_id}", response_model=AssetResponseDTO)
def get_asset_detail(asset_id: int):
    asset = next((a for a in assets if a["id"] == asset_id), None)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@app.put("/assets/{asset_id}", response_model=AssetResponseDTO)
def update_asset(asset_id: int, asset_data: AssetCreateDTO):
    asset = next((a for a in assets if a["id"] == asset_id), None)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    if any(a["serial_number"] == asset_data.serial_number and a["id"] != asset_id for a in assets):
        raise HTTPException(status_code=400, detail="Serial number already exists on another asset")
        
    asset.update(asset_data.model_dump())
    return asset

@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int):
    asset = next((a for a in assets if a["id"] == asset_id), None)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    assets.remove(asset)
    return {"status_code": 200, "message": f"Deleted asset {asset_id} successfully"}

@app.post("/allocations", response_model=AllocationResponseDTO, status_code=201)
def create_allocation(alloc_data: AllocationCreateDTO):
    if not re.match(EMAIL_REGEX, alloc_data.employee_email):
        raise HTTPException(status_code=400, detail="Invalid employee email format")

    asset = next((a for a in assets if a["id"] == alloc_data.asset_id), None)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found in company inventory")
        
    if asset["status"] != AssetStatus.READY:
        raise HTTPException(status_code=400, detail="Asset is not READY for allocation")
        
    if alloc_data.allocated_quantity > asset["stock_available"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Requested quantity exceeds available stock. Max available: {asset['stock_available']}"
        )
        
    asset["stock_available"] -= alloc_data.allocated_quantity
    
    if asset["stock_available"] == 0:
        asset["status"] = AssetStatus.ALLOCATED
        
    new_alloc_id = max((al["id"] for al in allocations), default=0) + 1
    new_allocation = {
        "id": new_alloc_id,
        "asset_id": alloc_data.asset_id,
        "employee_email": alloc_data.employee_email,
        "allocated_quantity": alloc_data.allocated_quantity,
        "start_date": alloc_data.start_date,
        "duration_months": alloc_data.duration_months
    }
    allocations.append(new_allocation)
    
    return new_allocation

@app.get("/allocations", response_model=List[AllocationResponseDTO])
def get_all_allocations():
    return allocations