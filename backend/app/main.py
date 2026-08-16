from fastapi import FastAPI

app = FastAPI(
    title="Hirely API",
    description="Backend API for Hirely",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Hirely API",
    }