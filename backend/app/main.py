from fastapi import FastAPI
from app.api.health import router as health_router

app = FastAPI(
    title="Hirely API",
    description="Backend API for Hirely",
    version="0.1.0"
)


app.include_router(health_router)