
# === backend/models.py ===
from pydantic import BaseModel
from typing import List

class AdminLogin(BaseModel):
    username: str
    password: str

class StudentRegister(BaseModel):
    name: str
    email: str
    password: str

class ContactForm(BaseModel):
    name: str
    email: str
    message: str
    
class StudentLogin(BaseModel):
    email: str
    password: str

class Question(BaseModel):
    topic: str
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str

class QuizSubmission(BaseModel):
    student_id: int
    topic: str
    answers: List[str]
    questions: List[int]