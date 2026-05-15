from fastapi import APIRouter
from app.schemas.load_object import LoadObjectRequest
from app.services.calculation import forward
from app.utils.response import success_response

router = APIRouter(prefix="/api/load-object", tags=["Load Object"])

@router.post("/calculate")
async def calculate_pole(payload: LoadObjectRequest):
    # Forward to Calculation after turn to snake_case format
    result = await forward("/api/load-object/calculate", payload)
    # print("data", result.data)
    return success_response(
        data=result.data,
        message=result.message,
        success=result.success,
        to_camel=True
    )
   