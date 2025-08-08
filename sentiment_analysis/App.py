from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import random
from transformers import pipeline

app = FastAPI()

# Initialize data
data_path = "edtech_adaptive_learning_dataset.csv"
try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        "user_id", "topic", "time_spent", "quiz_score", 
        "preference", "feedback", "rating"
    ])
    df.to_csv(data_path, index=False)

# Load sentiment analyzer
sentiment_analyzer = pipeline("sentiment-analysis")

# Pydantic models
class UserLearningData(BaseModel):
    user_id: int
    topic: str
    time_spent: int
    quiz_score: int
    preference: str
    feedback: str
    rating: int

class FeedbackText(BaseModel):
    feedback: str

# Root route to fix 404
@app.get("/")
def home():
    return {"message": "EdTech Sentiment Analysis API is running."}

# Submit learning data
@app.post("/submit_data")
def submit_learning_data(data: UserLearningData):
    global df
    new_data = pd.DataFrame([data.dict()])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(data_path, index=False)
    return {"message": "Data submitted successfully."}

# Recommendation system
@app.get("/get_recommendations/{user_id}")
def get_recommendations(user_id: int):
    user_data = df[df['user_id'] == user_id]
    if user_data.empty:
        return {"message": "User not found."}
    seen_topics = user_data['topic'].unique().tolist()
    all_topics = df['topic'].unique().tolist()
    unseen_topics = list(set(all_topics) - set(seen_topics))
    if not unseen_topics:
        unseen_topics = all_topics
    recommendations = random.sample(unseen_topics, k=min(3, len(unseen_topics)))
    return {"recommended_topics": recommendations}

# Feedback sentiment analysis
@app.post("/analyze_feedback")
def analyze_feedback(feedback: FeedbackText):
    result = sentiment_analyzer(feedback.feedback)
    return {"feedback_sentiment": result[0]}

# Adaptive assessment logic
@app.get("/adaptive_assessment/{user_id}")
def adaptive_assessment(user_id: int):
    user_data = df[df['user_id'] == user_id]
    if user_data.empty:
        return {"message": "User not found."}
    avg_score = user_data['quiz_score'].mean()
    if avg_score >= 80:
        difficulty = "Advanced"
    elif avg_score >= 50:
        difficulty = "Intermediate"
    else:
        difficulty = "Beginner"
    sample_questions = {
        "Beginner": ["What is 2 + 2?", "Define variable."],
        "Intermediate": ["Solve x: 2x + 5 = 15", "Explain slope in linear equations."],
        "Advanced": ["Differentiate f(x) = x^2 + 3x", "What is an eigenvector?"]
    }
    questions = sample_questions[difficulty]
    return {
        "assessment_level": difficulty,
        "questions": questions
    }

# Placeholder chatbot endpoint
@app.post("/chatbot")
async def chatbot(request: Request):
    data = await request.json()
    user_query = data.get("query")
    return {"reply": f"You asked: '{user_query}'. This is a placeholder reply."}
