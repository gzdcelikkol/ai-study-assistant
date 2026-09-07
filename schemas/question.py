# request & response objeleri
from typing import Literal, Optional
from pydantic import BaseModel

DifficultyLevel = Literal["eli5", "beginner", "intermediate", "academic"]
class QuestionRequest(BaseModel):
    question: str
    session_id: str = "default_student"
    mode: Literal["standard", "socratic"] = "standard"
    level: DifficultyLevel = "intermediate"

class VerificationResult(BaseModel):
        faithfulness_score: float
        is_grounded: bool
        hallucination_detected: bool
        reasoning: str

class QuestionResponse(BaseModel):
        session_id: str
        mode: str
        level: str
        question: str
        answer: str
        verification: VerificationResult