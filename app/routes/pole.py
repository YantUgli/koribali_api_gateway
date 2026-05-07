from fastapi import APIRouter
from app.schemas.pole import CalculationRequest, CalculationResponse
from app.services.calculation import forward
from app.lib.response import BaseResponse

router = APIRouter(prefix="/api/pole", tags=["Pole Calculation"])

@router.post("/calculate", response_model=BaseResponse)
async def calculate_pole(payload: CalculationRequest):
    print("payload: ", type(payload))
    return {
        "message" : "berhasil kirim payload",
        "data" : payload,
        "success" : True
            }
    # return await forward("/api/pole/calculate", payload )