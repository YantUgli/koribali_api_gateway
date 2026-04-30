import httpx
from pydantic import BaseModel
from fastapi import HTTPException, status
from app.core.config import settings
from app.core.security import get_internal_service_headers
from loguru import logger
from typing import Optional
from app.schemas.opening_part import OpeningPartResponse, OpeningPartResponseStatus

DEFAULT_SUCCESS_MESSAGE = "Calculation completed successfully"

async def forward(path: str, payload: BaseModel, status:Optional[str]= None) -> dict:
    url = f"{settings.calc_service_url}{path}"
    print(url)
    logger.info(f"Forwarding to {url}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload.model_dump(),
                headers=get_internal_service_headers(),
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            # print(status == "status", result)

            unique_code = result.get("unique_code")
            success_message = DEFAULT_SUCCESS_MESSAGE

            if unique_code == 1:
                success_message = "Hasil calculation sempurna"
            elif unique_code == 2:
                success_message = "Hasil calculation rawan"

            print(success_message)
            
            if status == "status":
                return OpeningPartResponseStatus(
                status = result.get("status", "success"),
                message = result.get("message", success_message),
                data = result.get("data")
            )

            return OpeningPartResponse(
                success = result.get("success", True),
                message = success_message,
                data = result.get("data"),
            )
        

    except httpx.HTTPStatusError as e:
        logger.error(f"Calculation service error: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail="Error from calculation service"
        )
    except httpx.RequestError as e:
        logger.error(f"Cannot reach calculation service: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Calculation service unavailable"
        )