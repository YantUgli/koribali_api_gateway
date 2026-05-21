from fastapi import APIRouter
from app.schemas.pole import CalculationRequest, CalculationResponse
from app.services.calculation import forward
from app.utils.response import success_response

router = APIRouter(prefix="/api/pole", tags=["Pole Calculation"])

@router.post("/calculate")
async def calculate_pole(payload: CalculationRequest):
    # Forward to Calculation after turn to snake_case format
    result = await forward("/api/pole/calculate", payload )
    return success_response(
        data=result.data,
        message=result.message,
        success=result.success,
        to_camel=True
    )
   