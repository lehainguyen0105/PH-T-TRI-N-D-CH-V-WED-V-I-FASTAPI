from sqlalchemy.orm import Session
from model import OrderModel

def get_order_by_id(db: Session, order_id: int):
    # Thay .one() bằng .first() để an toàn nếu id không tồn tại
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    return order