# app/services/staging_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.staging import StagingData
from app.schemas.load_object import LoadObjectRequest

# Tambahkan 'async' di definisi fungsi
async def save_to_staging(db: AsyncSession, payload: LoadObjectRequest, result_data: dict) -> str:
    payload_dict = payload.model_dump()
    project_data = payload_dict.pop("project", {})
    condition_data = payload_dict.pop("condition", {})
    
    dynamic_input = payload_dict
    
    new_staging = StagingData(
        project_title=project_data.get("project_title"),
        project_date=project_data.get("project_date"),
        report_number=project_data.get("report_number"),
        request_number=project_data.get("request_number"),
        design_standard=condition_data.get("design_standard"),
        design_wind_speed=condition_data.get("design_wind_speed"),
        design_air_density=condition_data.get("design_air_density"),
        calculation_input_payload=dynamic_input,
        calculation_result_payload=result_data,
        status="pending"
    )
    
    db.add(new_staging)
    
    # Gunakan await untuk commit dan refresh
    await db.commit()
    await db.refresh(new_staging)
    
    return new_staging.id