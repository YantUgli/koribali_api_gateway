from fastapi import APIRouter
from app.schemas.opening_part import OpeningPartRequest, OpeningPartResponse, OpeningPartResponseStatus
from app.services.calculation import forward

router = APIRouter(prefix="/api/opening-part", tags=["Opening Part"])

@router.post("/calculate", response_model=OpeningPartResponse)
async def calculate_opening_part(payload: OpeningPartRequest):
    return await forward("/api/opening-part/calculate", payload)


@router.post("/calculate-status", response_model=OpeningPartResponseStatus)
async def calculate_opening_part_status(payload: OpeningPartRequest):
    return await forward("/api/opening-part/calculate-status", payload, "status")
