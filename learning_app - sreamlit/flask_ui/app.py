from flask import Flask, render_template, request, redirect, flash
import requests

app = Flask(__name__)
app.secret_key = "somethingsecret"

FASTAPI_URL = "http://127.0.0.1:8000"

@app.route("/")
def home():
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_id = request.form["user_id"]
        name = request.form["name"]
        password = request.form["password"]

        response = requests.post(f"{FASTAPI_URL}/register", data={
            "user_id": user_id,
            "name": name,
            "password": password
        })

        if response.status_code == 200:
            flash("Registered successfully!", "success")
        else:
            flash("Registration failed!", "danger")
        return redirect("/register")

    return render_template("register.html")
