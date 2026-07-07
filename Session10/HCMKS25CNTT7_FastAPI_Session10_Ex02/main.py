from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from model import *
from order_service import get_order_by_id

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/orders/{order_id}")
def get_order_detail(order_id: int, db: Session = Depends(get_db)):
    # Gọi tầng service lấy đơn hàng
    order = get_order_by_id(db=db, order_id=order_id)
    
    # Nếu không tìm thấy (order là None), chủ động chặn lỗi và ném về 404 luôn
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Don hang khong ton tai"
        )
        
    return {
        "status_code": 200,
        "message": "Lay thong tin don hang thanh cong",
        "data": {
            "id": order.id,
            "customer_name": order.customer_name,
            "total_price": order.total_price
        }
    }