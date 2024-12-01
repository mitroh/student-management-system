from fastapi import FastAPI
from routes.students import router as student_router

app = FastAPI(
    title="Student Management System",
    description="Backend Intern Hiring Task - FastAPI + MongoDB",
    version="1.0.0"
)

app.include_router(student_router, prefix="/students", tags=["Students"])
