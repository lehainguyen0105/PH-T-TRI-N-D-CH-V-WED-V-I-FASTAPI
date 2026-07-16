from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Warehouse, Package, Waybill
from schemas import WarehouseCreate, PackageUpdate
from sqlalchemy.exc import SQLAlchemyError

def create_warehouse(db: Session, data: WarehouseCreate):
    try:
        new_warehouse = Warehouse(**data.model_dump())
        db.add(new_warehouse)
        db.commit()
        db.refresh(new_warehouse)
        return new_warehouse
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Lỗi cơ sở dữ liệu khi tạo mới nhà kho"
        )

def get_warehouse_detail(db: Session, warehouse_id: int):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if warehouse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Nhà kho không tồn tại"
        )
    return warehouse

def patch_package(db: Session, package_id: int, data: PackageUpdate):
    try:
        package = db.query(Package).filter(Package.id == package_id).first()
        if package is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Kiện hàng không tồn tại"
            )
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(package, key, value)
            
        db.commit()
        db.refresh(package)
        return package
    except HTTPException as he:
        raise he
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Lỗi cơ sở dữ liệu khi cập nhật thông tin kiện hàng"
        )

def delete_waybill(db: Session, waybill_id: int):
    try:
        waybill = db.query(Waybill).filter(Waybill.id == waybill_id).first()
        if waybill is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Vận đơn không tồn tại"
            )
        
        db.delete(waybill)
        db.commit()
        return waybill
    except HTTPException as he:
        raise he
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Lỗi cơ sở dữ liệu khi xóa vận đơn"
        )