# schemas/quiz.py
from pydantic import BaseModel

class GenerateQuizRequest(BaseModel):
    topic: str = "Veri Yapıları"

class EvaluateAnswerRequest(BaseModel):
    question: str
    user_answer: str