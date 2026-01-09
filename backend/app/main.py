from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.quiz import router as quiz_router
from app.api.routes.health import router as health_router
from app.api.routes.config import router as config_router
from app.api.routes.data import router as data_router

app = FastAPI(title="QuizForge API")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(config_router)
app.include_router(data_router)
app.include_router(quiz_router)
