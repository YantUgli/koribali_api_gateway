from pydantic import BaseModel
from typing import Any

class BaseResponse(BaseModel):
    data : Any
    success : bool
    message : str


