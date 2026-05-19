from app.utils.base_schema import CamelBaseModel
from typing import List, Dict, Optional


class PoleSchema(CamelBaseModel):
    name: str
    diameter: float
    thickness: float
    material: str
    z_height: float


class DirectObjectSchema(CamelBaseModel):
    name: str
    area: float
    cf: float
    weight: float
    z_height: float


class ProjectSchema(CamelBaseModel):
    report_number: str
    project_title: str
    project_date: str
    request_number: str

class ConditionSchema(CamelBaseModel):
    design_standard: str
    design_wind_speed: float
    design_air_density: float

class LoadObjectRequest(CamelBaseModel):
    project: ProjectSchema
    condition: ConditionSchema
    poles: List[PoleSchema]
    high_evaluation: Dict[str, float]
    direct_objects: Optional[List[DirectObjectSchema]] = []
    session_id: Optional[str] = None