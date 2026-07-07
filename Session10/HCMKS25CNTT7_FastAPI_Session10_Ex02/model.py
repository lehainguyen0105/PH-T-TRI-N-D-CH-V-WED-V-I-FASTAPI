from database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100), nullable=False)
    total_price = Column(Integer, nullable=False)

class OrderResponseDTO(BaseModel):
    id: int
    customer_name: str
    total_price: int