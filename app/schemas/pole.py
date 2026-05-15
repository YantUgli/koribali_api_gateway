from typing import List
from app.utils.base_schema import CamelBaseModel

# Inherit dari CamelBaseModel
class PoleInput(CamelBaseModel):
    diameter_pole: float
    height_pole: float
    lowest_height_pole: float
    thickness_pole: float
    material_pole: str


class DoObject(CamelBaseModel):
    area_front_do: float
    area_side_do: float
    cf_do: float
    height_do: float
    weight_do: float
    name_do: str


class CalculationRequest(CamelBaseModel):
    pole: PoleInput
    objects: List[DoObject]


class CalculationResponse(CamelBaseModel):
    message: str
    input: CalculationRequest
