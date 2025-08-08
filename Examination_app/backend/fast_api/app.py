from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import sqlite3
import os
from database import init_db, DB_NAME
from models import *
from llama_utils import stream_response  # kept for llama-based generation

from transformers import pipeline  # ✅ Added
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")  # ✅ Added

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/admin/login")
def admin_login(data: AdminLogin):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (data.username, data.password))
    admin = cursor.fetchone()
    conn.close()
    if admin:
        return {"status": "success", "admin_id": admin[0]}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/admin/upload-csv")
def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    conn = sqlite3.connect(DB_NAME)
    df.to_sql("questions", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Questions uploaded"}

@app.post("/student/register")
def student_register(data: StudentRegister):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (name, email, password) VALUES (?, ?, ?)", (data.name, data.email, data.password))
        conn.commit()
        return {"status": "success"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    finally:
        conn.close()

@app.post("/student/login")
def student_login(data: StudentLogin):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE email=? AND password=?", (data.email, data.password))
    student = cursor.fetchone()
    conn.close()
    if student:
        return {"status": "success", "student_id": student[0], "name": student[1]}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/quiz/questions/{topic}")
def get_quiz_questions(topic: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE topic=? ORDER BY RANDOM() LIMIT 10", (topic,))
    questions = cursor.fetchall()
    conn.close()
    return [{
        "id": q[0],
        "question_text": q[2], 
        "option_a": q[3],
        "option_b": q[4],
        "option_c": q[5],
        "option_d": q[6],
    } for q in questions]

@app.post("/quiz/submit")
def submit_quiz(data: QuizSubmission):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    score = 0
    incorrect = []
    for qid, ans in zip(data.questions, data.answers):
        cursor.execute("SELECT correct_answer, question FROM questions WHERE id=?", (qid,))
        correct, question = cursor.fetchone()
        if ans == correct:
            score += 1
        else:
            incorrect.append(question)

    # ✅ Replaced llama feedback with transformers feedback
    feedback_text = f"You answered {score} out of {len(data.questions)} questions correctly."
    sentiment_result = sentiment_pipeline(feedback_text)[0]
    feedback = f"{feedback_text} Sentiment: {sentiment_result['label']} ({sentiment_result['score']:.2f})"

    cursor.execute("INSERT INTO results (student_id, topic, score, feedback) VALUES (?, ?, ?, ?)", (data.student_id, data.topic, score, feedback))
    conn.commit()
    conn.close()
    return {"score": score, "feedback": feedback}

@app.get("/admin/students")
def view_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return [{"id": s[0], "name": s[1], "email": s[2]} for s in students]

@app.get("/admin/performance")
def view_performance():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT students.name, results.topic, results.score FROM results JOIN students ON students.id = results.student_id")
    records = cursor.fetchall()
    conn.close()
    return [{"name": r[0], "topic": r[1], "score": r[2]} for r in records]

@app.post("/contact")
def submit_contact(data: ContactForm):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contact (name, email, message) VALUES (?, ?, ?)",
                   (data.name, data.email, data.message))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Contact form submitted"}

@app.get("/student/results/{student_id}")
def get_student_results(student_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT topic, score, feedback FROM results WHERE student_id=? ORDER BY id DESC",
        (student_id,)
    )
    records = cursor.fetchall()
    conn.close()
    return [{"topic": r[0], "score": r[1], "feedback": r[2]} for r in records]

@app.post("/admin/call_llama_create_questions")
def generate_questions(topic: str = Form(...)):
    prompt = f"""
Generate 100 multiple-choice questions (MCQs) for the topic: {topic}.
Each question should have:
1. question
2. option_a
3. option_b
4. option_c
5. option_d
6. correct_answer (A/B/C/D)

Respond in JSON list format like this:
[
  {{
    "topic": "TopicName",
    "question": "What is...",
    "option_a": "Option A",
    "option_b": "Option B",
    "option_c": "Option C",
    "option_d": "Option D",
    "correct_answer": "A"
  }},
  ...
]
"""
    try:
        raw = stream_response(prompt)
        import json
        questions = json.loads(raw)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        for q in questions:
            cursor.execute('''
                INSERT INTO questions (topic, question, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                q['topic'], q['question'], q['option_a'], q['option_b'],
                q['option_c'], q['option_d'], q['correct_answer']
            ))

        conn.commit()
        conn.close()

        return {"status": "success", "inserted": len(questions)}

    except Exception as e:
        return {"status": "error", "message": str(e)}

#D:\PROJECTS\Examination_app\backend\fast_api>uvicorn app:app --reload