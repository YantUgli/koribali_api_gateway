from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.load_object import LoadObjectRequest
from app.services.calculation import forward
from app.utils.response import success_response
from app.services.staging_service import save_to_staging
from app.core.staging_database import get_db
from app.utils.sql_staging.orchestrator import Orchestrator

router = APIRouter(prefix="/api/load-object", tags=["Load Object"])

@router.post("/calculate")
async def calculate_pole(payload: LoadObjectRequest, db:AsyncSession = Depends(get_db)):
    # Forward to Calculation after turn to snake_case format
    final_data = await Orchestrator.run_calculation_and_staging(
        calc_url="/api/load-object/calculate",
        payload=payload, 
        db=db
    )

    print("this is payload: ", payload.session_id)


    return success_response(
        data=final_data["data"],
        message=final_data["message"], 
        success=final_data["success"], 
        to_camel=True
    )