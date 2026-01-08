from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.utils.yaml_loader import load_quiz_from_yaml, QuizLoadError
from app.models.quiz_models import Quiz

router = APIRouter(prefix="/quiz", tags=["quiz"])

# In-memory quiz state (v1)
_loaded_quiz: Quiz | None = None


class LoadQuizRequest(BaseModel):
    path: str


class LoadQuizResponse(BaseModel):
    title: str
    num_questions: int


@router.post("/load", response_model=LoadQuizResponse)
def load_quiz(request: LoadQuizRequest):
    global _loaded_quiz

    try:
        quiz = load_quiz_from_yaml(request.path)
    except QuizLoadError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    _loaded_quiz = quiz

    return LoadQuizResponse(
        title=quiz.title,
        num_questions=len(quiz.questions)
    )