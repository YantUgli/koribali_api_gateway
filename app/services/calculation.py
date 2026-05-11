import httpx
from pydantic import BaseModel
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.security import get_internal_service_headers
from loguru import logger
from typing import Optional
from app.schemas.opening_part import OpeningPartResponse, OpeningPartResponseStatus
from app.utils.message_response import get_message_by_unique_code 

async def forward(path: str, payload: BaseModel) -> dict:
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
            success_message = get_message_by_unique_code(unique_code)

            return OpeningPartResponse(
                success = result.get("success", True),
                message = success_message,
                data = result.get("data"),
            )
        

    except httpx.HTTPStatusError as e:
        logger.error(f"Calculation service error: {e.response.status_code}")
        try:
            flask_response = e.response.json()
        except Exception:
            flask_response = {"detail": e.response.text}

        # Menggunakan HTTPExeption dari FastAPI, akan masuk kedalam detail
        # raise HTTPException(
        #     status_code=e.response.status_code,
        #     detail=flask_response  # teruskan langsung, jangan replace
        # )

        # Cukup menggunakan JSONResponse
        return JSONResponse(
            status_code=response.status_code,
            content=flask_response
        )


    except httpx.RequestError as e:
        logger.error(f"Cannot reach calculation service: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Calculation service unavailable"
        )