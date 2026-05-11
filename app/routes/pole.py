from fastapi import APIRouter
from app.schemas.pole import CalculationRequest, CalculationResponse
from app.services.calculation import forward
from app.utils.response import BaseResponse

router = APIRouter(prefix="/api/pole", tags=["Pole Calculation"])

@router.post("/calculate", response_model=BaseResponse)
async def calculate_pole(payload: CalculationRequest):
    # Forward to Calculation after turn to snake_case format
    return await forward("/api/pole/calculate", payload )