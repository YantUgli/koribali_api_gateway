from pydantic import BaseModel, Field
from typing import List

class PoleInput(BaseModel):
    diameter_pole : float = Field(alias="diameterPole")
    height_pole : float = Field(alias="heightPole")
    lowest_height_pole : float = Field(alias="lowestHeightPole")
    thickness_pole : float = Field(alias="thicknessPole")
    material_pole : str = Field(alias="materialPole")

class DoObject(BaseModel):
    area_front_do : float = Field(alias="areaFrontDo")
    area_side_do : float = Field(alias="areaSideDo")
    cf_do : float = Field(alias="cfDo")
    height_do : float = Field(alias="heightDo")
    weight_do : float = Field(alias="weightDo")
    name_do : str = Field(alias="nameDo")

# kedua Model
class CalculationRequest(BaseModel):
    pole : PoleInput
    objects : List[DoObject]

class CalculationResponse(BaseModel):
    message:str
    input : CalculationRequest