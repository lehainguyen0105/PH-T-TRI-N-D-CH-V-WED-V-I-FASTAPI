from pydantic import BaseModel

class RoleResponse(BaseModel):
    """Schema trả về thông tin của một Role."""
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
