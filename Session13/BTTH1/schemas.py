from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Any
from datetime import datetime, timezone

class Status(str, Enum):
    AVAILABLE = "AVAILABLE"
    OUT_OF_STOCK = "OUT_OF_STOCK"

class MenuRequest(BaseModel):
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: Status

class MenuResponse(BaseModel):
    id: int
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class StandardResponse(BaseModel):
    statusCode: int
    data: Any | None =None
    error: Any | None =None
    message: str
    path: str
    timestamp: str

def standard_response(status_code: int, data: Any,error: Any, message: str, path: str):
    content_response = StandardResponse(
        statusCode=status_code,
        data=data,
        error=error,
        message=message,
        path=path,
        timestamp=datetime.now(timezone.utc).isoformat()
    ).model_dump()

    return JSONResponse(
        status_code=status_code,
        content=content_response
    )