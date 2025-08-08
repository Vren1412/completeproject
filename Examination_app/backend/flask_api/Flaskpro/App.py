from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"
API_URL = "http://localhost:8000"

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        contact_entry = Contact(name=name, email=email, message=message)
        db.session.add(contact_entry)
        db.session.commit()

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for("home"))

    return render_template("contact.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        res = requests.post(f"{API_URL}/admin/login", json={"username": username, "password": password})
        if res.status_code == 200:
            session["admin_id"] = res.json()["admin_id"]
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))
    return render_template("admin_dashboard.html")

@app.route("/student/register", methods=["GET", "POST"])
def student_register():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"]
        }
        res = requests.post(f"{API_URL}/student/register", json=data)
        if res.status_code == 200:
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("student_login"))
        else:
            flash(res.json()["detail"], "danger")
    return render_template("student_register.html")

@app.route("/student/login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        res = requests.post(f"{API_URL}/student/login", json={"email": email, "password": password})
        if res.status_code == 200:
            data = res.json()
            session["student_id"] = data["student_id"]
            session["student_name"] = data["name"]
            return redirect(url_for("start_quiz"))
        else:
            flash(res.json()["detail"], "danger")
    return render_template("student_login.html")

@app.route("/student/quiz", methods=["GET", "POST"])
def start_quiz():
    if "student_id" not in session:
        return redirect(url_for("student_login"))

    if request.method == "POST":
        topic = request.form["topic"]
        res = requests.get(f"{API_URL}/quiz/questions/{topic}")
        if res.status_code == 200:
            questions = res.json()
            return render_template("quiz.html", questions=questions, topic=topic)
        else:
            flash("No questions found for this topic.", "danger")

    return render_template("quiz_topic.html")

@app.route("/student/submit", methods=["POST"])
def submit_quiz():
    answers = []
    questions = []
    for key, val in request.form.items():
        if key.startswith("q_"):
            qid = int(key.split("_")[1])
            questions.append(qid)
            answers.append(val)

    topic = request.form["topic"]
    res = requests.post(f"{API_URL}/quiz/submit", json={
        "student_id": session["student_id"],
        "topic": topic,
        "questions": questions,
        "answers": answers
    })

    if res.status_code == 200:
        result = res.json()
        return render_template("result.html", score=result["score"], feedback=result["feedback"])
    else:
        flash("Submission failed.", "danger")
        return redirect(url_for("start_quiz"))

@app.route("/student/results")
def view_results():
    res = requests.get(f"{API_URL}/student/results/{session['student_id']}")
    if res.status_code == 200:
        results = res.json()
        return render_template("results.html", results=results)
    else:
        flash("Could not load results.", "danger")
        return redirect(url_for("start_quiz"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
#"C:\Users\ASUS\AppData\Local\Programs\Python\Python313\python.exe" App.py
