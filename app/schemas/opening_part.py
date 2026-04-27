from pydantic import BaseModel, Field

class OpeningPartRequest(BaseModel):
    width: float = Field(..., gt=0, description="Width in mm")
    height: float = Field(..., gt=0, description="Height in mm")
    thickness: float = Field(..., gt=0, description="Thickness in mm")

class OpeningPartResponse(BaseModel):
    area: float
    perimeter: float
    status: str