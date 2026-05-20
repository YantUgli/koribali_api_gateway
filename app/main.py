from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging
from app.routes import opening_part, pole, load_object

# Database Needs
from app.core.staging_database import engine, Base
from app.models.staging import StagingProject

# setup logging saat app start
setup_logging()

# Staging Database
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dijalankan saat startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield # Aplikasi berjalan
    
    # Jika ada logika shutdown, letakkan di sini
    await engine.dispose()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API Gateway",
    lifespan= lifespan
)


# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # bisa diganti url agar lebih spesifik
    allow_credentials=False,  # harus False kalau allow_origins="*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# register router
app.include_router(opening_part.router)
app.include_router(pole.router)
app.include_router(load_object.router)


# health check
@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name}