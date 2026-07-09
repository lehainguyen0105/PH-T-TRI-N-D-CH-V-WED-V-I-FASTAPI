from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
from typing import Any
from datetime import datetime, timezone

class RoomSize(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class SlotStatus(str, Enum):
    VACANT = "VACANT"
    OCCUPIED = "OCCUPIED"

class SlotRequest(BaseModel):
    slot_number: str
    room_size: RoomSize
    price_per_day: float = Field(..., gt=0.0)
    status: SlotStatus

class SlotResponse(BaseModel):
    id: int
    slot_number: str
    room_size: str
    price_per_day: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class StandardResponse(BaseModel):
    statusCode: int
    data: Any | None = None
    error: Any | None = None
    message: str
    path: str
    timestamp: str

def standard_response(status_code: int, data: Any, error: Any, message: str, path: str):
    content_response = StandardResponse(
        statusCode=status_code,
        data=data,
        error=error,
        message=message,
        path=path,
        timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    ).model_dump()

    return JSONResponse(
        status_code=status_code,
        content=content_response
    )