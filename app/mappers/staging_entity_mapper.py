# app/mappers/staging_entity_mapper.py
from datetime import datetime
from app.schemas.load_object import LoadObjectRequest
from app.models.staging import (
    StagingProject, StagingCondition, StagingStepPole, 
    StagingHighEval, StagingDirectObject
)

class StagingEntityMapper:
    @staticmethod
    def map_to_entities(payload: LoadObjectRequest, calc_result: dict) -> StagingProject:
        # Parsing date dari string ke Date object (YYYY-MM-DD)
        proj_date = datetime.strptime(payload.project.project_date, "%Y-%m-%d").date() if payload.project.project_date else None

        # 1. Buat Parent (project)
        project_entity = StagingProject(
            title=payload.project.project_title,
            date=proj_date,
            report_number=payload.project.report_number,
            # Note: project_type disesuaikan dgn schema jika ada
            calculation_result=calc_result
        )

        # 2. Buat Relasi Condition 1:1
        project_entity.condition = StagingCondition(
            design_standard=payload.condition.design_standard,
            wind_speed=payload.condition.design_wind_speed,
            air_density=payload.condition.design_air_density
        )

        # 3. Mapping (1:N) untuk list
        project_entity.poles = [
            StagingStepPole(
                name=p.name, diameter=p.diameter, thickness=p.thickness,
                height=p.z_height, material=p.material, quantity=1 
            ) for p in payload.poles
        ]
        
        # 4. pengecheckan apakah ada direct object kalau ada = step 3
        if payload.direct_objects:
            project_entity.direct_objects = [
                StagingDirectObject(
                    name=obj.name, front_area=obj.area, side_area=obj.area,
                    height=obj.z_height, weight=obj.weight, coefficient=obj.cf, quantity=1
                ) for obj in payload.direct_objects
            ]
            
        # dapat menangkap key-value dict: {"baseCheck": 0.0}
        project_entity.high_evals = [
            StagingHighEval(name=key, point_evaluate=val)
            for key, val in payload.high_evaluation.items()
        ]

        return project_entity