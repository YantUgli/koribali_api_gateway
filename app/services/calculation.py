import httpx
from pydantic import BaseModel
from fastapi import HTTPException, status
from app.core.config import settings
from loguru import logger

async def forward(path: str, payload: BaseModel) -> dict:
    url = f"{settings.calc_service_url}{path}"

    logger.info(f"Forwarding to {url}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload.model_dump(),
                headers={"X-Internal-Key": settings.calc_service_key},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

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