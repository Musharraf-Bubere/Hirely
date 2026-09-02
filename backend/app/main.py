from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.core.config import settings

from app.api.recruiter import router as recruiter_router
from app.api.candidate import router as candidate_router
from app.api.jobs import router as jobs_router
from app.api.applications import router as applications_router
from app.api.candidate_skills import router as candidate_skills_router
from app.api.job_skills import router as job_skills_router


app = FastAPI(
    title=settings.app_name,
    description="Backend API for Hirely",
    version=settings.app_version,
    debug=settings.debug,
)


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(recruiter_router)
app.include_router(candidate_router)
app.include_router(candidate_skills_router)
app.include_router(jobs_router)
app.include_router(applications_router)
app.include_router(job_skills_router)