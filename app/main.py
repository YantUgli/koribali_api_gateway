from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.routes import opening_part

# setup logging saat app start
setup_logging()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API Gateway"
)

# register router
app.include_router(opening_part.router)


# health check
@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name}