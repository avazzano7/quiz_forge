from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.utils.yaml_loader import load_quiz_from_yaml, QuizLoadError
from app.models.quiz_models import Quiz

router = APIRouter(prefix="/quiz", tags=["quiz"])

# In-memory quiz state (v1)
_loaded_quiz: Quiz | None = None
_user_answers: dict[int, int] = {}


class LoadQuizRequest(BaseModel):
    path: str


class LoadQuizResponse(BaseModel):
    title: str
    num_questions: int


class QuestionResponse(BaseModel):
    id: int
    question: str
    choices: list[str]


class AnswerRequest(BaseModel):
    question_id: int
    choice_index: int


class AnswerResponse(BaseModel):
    correct: bool


class ScoreResponse(BaseModel):
    score: int
    total: int


@router.post("/load", response_model=LoadQuizResponse)
def load_quiz(request: LoadQuizRequest):
    global _loaded_quiz, _user_answers

    try:
        quiz = load_quiz_from_yaml(request.path)
    except QuizLoadError as e:
        raise HTTPException(status_code=400, detail=str(e))

    _loaded_quiz = quiz
    _user_answers = {}

    return LoadQuizResponse(
        title=quiz.title,
        num_questions=len(quiz.questions)
    )


@router.get("/question/{index}", response_model=QuestionResponse)
def get_question(index: int):
    if _loaded_quiz is None:
        raise HTTPException(
            status_code=400,
            detail="No quiz loaded. Please load a quiz first."
        )

    if index < 0 or index >= len(_loaded_quiz.questions):
        raise HTTPException(
            status_code=404,
            detail="Question index out of range."
        )

    q = _loaded_quiz.questions[index]

    return QuestionResponse(
        id=q.id,
        question=q.question,
        choices=q.choices,
    )


@router.post("/answer", response_model=AnswerResponse)
def submit_answer(request: AnswerRequest):
    if _loaded_quiz is None:
        raise HTTPException(
            status_code=400,
            detail="No quiz loaded. Please load a quiz first."
        )

    question = next(
        (q for q in _loaded_quiz.questions if q.id == request.question_id),
        None
    )

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question ID not found in the loaded quiz."
        )

    if request.choice_index < 0 or request.choice_index >= len(question.choices):
        raise HTTPException(
            status_code=400,
            detail="Choice index out of range."
        )

    _user_answers[question.id] = request.choice_index

    return AnswerResponse(
        correct=request.choice_index == question.correct_answer
    )


@router.get("/score", response_model=ScoreResponse)
def get_score():
    if _loaded_quiz is None:
        raise HTTPException(
            status_code=400,
            detail="No quiz loaded. Please load a quiz first."
        )

    score = sum(
        1
        for q in _loaded_quiz.questions
        if _user_answers.get(q.id) == q.correct_answer
    )

    return ScoreResponse(
        score=score,
        total=len(_loaded_quiz.questions)
    )
