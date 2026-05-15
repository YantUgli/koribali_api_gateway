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


class LoadObjectRequest(CamelBaseModel):
    poles: List[PoleSchema]
    high_evaluation: Dict[str, float]
    direct_objects: Optional[List[DirectObjectSchema]] = []