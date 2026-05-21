from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.load_object import LoadObjectRequest, LoadObjectResponse, StagingDataResponseSchema
from app.utils.response import success_response
from app.core.staging_database import get_db
from app.utils.sql_staging.orchestrator import Orchestrator

router = APIRouter(prefix="/api/load-object", tags=["Load Object"])

@router.post("/calculate", response_model=LoadObjectResponse)
async def calculate_pole(payload: LoadObjectRequest, db:AsyncSession = Depends(get_db)):
    # Forward to Calculation after turn to snake_case format
    final_data = await Orchestrator.run_calculation_and_staging(
        calc_url="/api/load-object/calculate",
        payload=payload, 
        db=db
    )

    return success_response(
        data=final_data["data"],
        message=final_data["message"], 
        success=final_data["success"], 
        to_camel=True
    )


@router.get("/{session_id}", response_model=StagingDataResponseSchema)
async def get_calculation_data(session_id: str, db: AsyncSession = Depends(get_db)):
    data = await Orchestrator.get_staging_data(session_id, db)
    
    if not data:
        raise HTTPException(status_code=404, detail="Session ID not found")
        
    return success_response(
        data=data,
        message="Staging data retrieved successfully",
        success=True,
        to_camel=True
    )