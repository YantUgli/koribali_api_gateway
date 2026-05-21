# app/mappers/staging_entity_mapper.py
from datetime import datetime
from app.schemas.load_object import LoadObjectRequest
from app.models.staging import (
    StagingProject, StagingCondition, StagingStepPole, 
    StagingHighEval, StagingDirectObject, 
    StagingCalculationResult,StagingPoleResult, StagingDirectObjectResult
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
        )

        # 2. Buat Relasi Condition 1:1
        project_entity.condition = StagingCondition(
            design_standard=payload.condition.design_standard,
            wind_speed=payload.condition.design_wind_speed,
            air_density=payload.condition.design_air_density
        )

        # 3. mapping input & simpan referensi dictionary
        poles_map = {} 
        for p in payload.poles:
            pole_entity = StagingStepPole(
                name=p.name, diameter=p.diameter, thickness=p.thickness,
                height=p.z_height, material=p.material, quantity=1 
            )
          
            project_entity.poles.append(pole_entity)
            poles_map[p.name] = pole_entity 

        direct_objs_map = {} 
        if payload.direct_objects:
            for obj in payload.direct_objects:
                do_entity = StagingDirectObject(
                    name=obj.name, front_area=obj.area, side_area=obj.area,
                    height=obj.z_height, weight=obj.weight, coefficient=obj.cf, quantity=1
                )
                project_entity.direct_objects.append(do_entity)
                direct_objs_map[obj.name] = do_entity
            

        # 4. arrange evaluasi dan hasil kalkulasi
        for eval_name, eval_point in payload.high_evaluation.items():
            
            # A. Buat Entitas High Eval (Input)
            eval_entity = StagingHighEval(name=eval_name, point_evaluate=eval_point)
            
            # B. Ambil data hasil kalkulasi dari Flask untuk evaluasi ini
            eval_result_data = calc_result.get(eval_name, {})
            
            # C. Buat Entitas Result Utama
            calc_result_entity = StagingCalculationResult(
                total_windload=eval_result_data.get("total_windload", 0.0),
                total_moment=eval_result_data.get("total_moment", 0.0),
                status=eval_result_data.get("status", "ok").lower()
            )
            
            # D. Mapping Pole Results (Relasi Berlian)
            for obj_res in eval_result_data.get("objects", []):
                obj_name = obj_res.get("name")
                
                # check pole
                related_pole = poles_map.get(obj_name) 
                if related_pole:
                    pole_res_entity = StagingPoleResult(
                        windload=obj_res.get("windload", 0.0),
                        moment=obj_res.get("moment", 0.0)
                    )
                    pole_res_entity.step_pole = related_pole 
                    calc_result_entity.pole_results.append(pole_res_entity)
                    continue 

                # check direct object
                related_do = direct_objs_map.get(obj_name) 
                if related_do:
                    do_res_entity = StagingDirectObjectResult(
                        windload=obj_res.get("windload", 0.0),
                        moment=obj_res.get("moment", 0.0)
                    )
                    do_res_entity.direct_object = related_do 
                    calc_result_entity.direct_object_results.append(do_res_entity)

            # F. Sambungkan semua dan masukkan ke Project
            eval_entity.calculation_result = calc_result_entity
            project_entity.high_evals.append(eval_entity)


        return project_entity