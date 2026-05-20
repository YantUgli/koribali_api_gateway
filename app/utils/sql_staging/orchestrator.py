from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.load_object import LoadObjectRequest
from app.services.calculation import forward
# from app.services.staging_service import save_to_staging
from app.utils.sql_staging.mapper import Mapper

from app.mappers.staging_entity_mapper import StagingEntityMapper
from app.repositories.staging_repository import StagingRepository
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
        print("this is ORCESTRATOR", type(result))
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