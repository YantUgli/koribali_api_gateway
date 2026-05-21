from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.schemas.load_object import LoadObjectRequest, StagingDataResponseSchema
from app.services.calculation import forward
# from app.services.staging_service import save_to_staging
from app.utils.sql_staging.mapper import Mapper

from app.mappers.staging_entity_mapper import StagingEntityMapper
from app.repositories.staging_repository import StagingRepository
from app.models.staging import StagingProject, StagingHighEval, StagingCalculationResult, StagingPoleResult, StagingDirectObjectResult

# Function Mapping Input Database Staging
def map_pole_result(p):
    pole = p.step_pole

    return {
        "type": "pole",
        "name": pole.name if pole else "Unknown Pole",
        "moment": p.moment,
        "windload": p.windload,

        # input data
        "diameter": pole.diameter if pole else None,
        "thickness": pole.thickness if pole else None,
        "material": pole.material if pole else None,
        "Height": pole.height if pole else None,
    }


def map_direct_object_result(d):
    obj = d.direct_object

    return {
        "type": "direct_object",
        "name": obj.name if obj else "Unknown Object",
        "moment": d.moment,
        "windload": d.windload,

        # input data
        "front_area": obj.front_area if obj else None,
        "side_area": obj.side_area if obj else None,
        "coefficient": obj.coefficient if obj else None,
        "weight": obj.weight if obj else None,
    }



class Orchestrator:
    
    @staticmethod
    async def run_calculation_and_staging(
        payload: LoadObjectRequest, 
        db: AsyncSession,
        calc_url : str
    ) -> dict:
        """
        Mengorkestrasi alur pemisahan data, pemanggilan calculation dengan mempertahankan 
        konvensi message & success asli, dan penyimpanan ke staging database.
        """
        # 1. Pemisahan Payload via Mapper
        pure_calculation_payload = Mapper.to_pure_calculation_payload(payload)
        
        # 2. Forward Pure Data ke Calculation Service
        result = await forward(calc_url, pure_calculation_payload)
        calculation_result = result.data if result.data else {}

        # 3. Translasi ke Entity Relational
        db_entity = StagingEntityMapper.map_to_entities(payload, calculation_result)
        
        # 4. Simpan ke Staging Layer
        session_id = await StagingRepository.save_staging_transaction(db, db_entity)
        
        # 5. Susun susunan data untuk Response Frontend
        final_data = Mapper.to_frontend_response_layout(
            calculation_result=calculation_result,
            session_id=session_id
        )
        
        # 6. Bungkus kembali message dan success asli dari microservice
        return {
            "data": final_data,
            "message": result.message, 
            "success": result.success  
        }
    
    @staticmethod
    async def get_staging_data(session_id: str, db: AsyncSession):
        stmt = select(StagingProject).where(StagingProject.id == session_id).options(
        selectinload(StagingProject.condition),
        selectinload(StagingProject.high_evals)
            .selectinload(StagingHighEval.calculation_result)
                .selectinload(StagingCalculationResult.pole_results)
                    .selectinload(StagingPoleResult.step_pole), 
        selectinload(StagingProject.high_evals)
            .selectinload(StagingHighEval.calculation_result)
                .selectinload(StagingCalculationResult.direct_object_results)
                    .selectinload(StagingDirectObjectResult.direct_object) 
    )
        
        result = await db.execute(stmt)
        project = result.scalar_one_or_none()
        
        if not project:
            return None
        
        high_eval_dict = {}
        
        for h in project.high_evals:
            # Akses calculation result
            calc = h.calculation_result
            
            # Mapping poles dan direct objects menjadi satu list "objects"
            objects = []
            
            if calc:
                # Add Pole Results
                objects.extend(
                    map_pole_result(p)
                    for p in calc.pole_results
                )
                
                # Add Direct Object Results
                objects.extend(
                    map_direct_object_result(p)
                    for p in calc.direct_object_results
                )

            high_eval_dict[h.name] = {
                "status": calc.status if calc else "N/A",
                "totalMoment": calc.total_moment if calc else 0.0,
                "totalWindload": calc.total_windload if calc else 0.0,
                "zRef": h.point_evaluate, 
                "objects": objects
            }
        
        response_data = StagingDataResponseSchema(
            project={
                "title": project.title,
                "report_number": project.report_number,
                "date": project.date, 
                "project_type": project.project_type
            },
            condition={
                "design_standard": project.condition.design_standard,
                "wind_speed": project.condition.wind_speed,
                "air_density": project.condition.air_density
            },
            high_evaluations=high_eval_dict
        )

        return response_data.model_dump(mode="json")