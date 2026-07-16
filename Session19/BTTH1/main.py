from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import services
import schemas

app = FastAPI(
    title="HỆ THỐNG QUẢN LÝ CHUỖI CUNG ỨNG"
)

Base.metadata.create_all(bind=engine)

@app.post(
    "/warehouses", 
    response_model=schemas.WarehouseDetailResponse, 
    status_code=status.HTTP_201_CREATED, 
    tags=["Warehouses"]
)
def create_warehouse(data: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    result = services.create_warehouse(db, data)
    return result

@app.get(
    "/warehouses/{warehouse_id}", 
    response_model=schemas.WarehouseDetailResponse, 
    status_code=status.HTTP_200_OK, 
    tags=["Warehouses"]
)
def get_warehouse_detail(warehouse_id: int, db: Session = Depends(get_db)):
    result = services.get_warehouse_detail(db, warehouse_id)
    return result

@app.patch(
    "/packages/{package_id}", 
    response_model=schemas.PackageResponse, 
    status_code=status.HTTP_200_OK, 
    tags=["Packages"]
)
def patch_package(package_id: int, data: schemas.PackageUpdate, db: Session = Depends(get_db)):
    result = services.patch_package(db, package_id, data)
    return result

@app.delete(
    "/waybills/{waybill_id}", 
    status_code=status.HTTP_200_OK, 
    tags=["Waybills"]
)
def delete_waybill(waybill_id: int, db: Session = Depends(get_db)):
    services.delete_waybill(db, waybill_id)
    return {
        "message": "Xóa vận đơn chi tiết thành công"
    }