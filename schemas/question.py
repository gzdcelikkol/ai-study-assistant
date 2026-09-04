# request & response objeleri
from typing import Literal
from pydantic import BaseModel

DifficultyLevel = Literal["eli5", "beginner", "intermediate", "academic"]
class QuestionRequest(BaseModel):
    question: str
    session_id: str = "default_student"
    mode: Literal["standard", "socratic"] = "standard"
    level: DifficultyLevel = "intermediate"