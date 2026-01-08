from pydantic import BaseModel, Field, field_validator
from typing import List


class Question(BaseModel):
    id: int
    question: str
    choices: List[str]
    correct_answer: int

    @field_validator('choices')
    @classmethod
    def validate_choices(cls, v):
        if len(v) < 2:
            raise ValueError('Each question must have at least two choices')
        return v

    @field_validator('correct_answer')
    @classmethod
    def validate_correct_answer(cls, v, info):
        choices = info.data.get('choices', [])
        if v < 0 or v >= len(choices):
            raise ValueError('correct_answer must be a valid index into choices')
        return v
    

class Quiz(BaseModel):
    title: str = Field(..., min_length=1)
    questions: List[Question]

    @field_validator('questions')
    @classmethod
    def validate_questions(cls, v):
        if not v:
            raise ValueError('Quiz must contain at least one question')
        
        ids = [q.id for q in v]
        if len(ids) != len(set(ids)):
            raise ValueError('Question IDs must be unique within a quiz')
        
        return v