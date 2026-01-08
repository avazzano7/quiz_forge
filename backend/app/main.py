from fastapi import FastAPI
from app.api.quiz import router as quiz_router

app = FastAPI(title="QuizForge API")

app.include_router(quiz_router)