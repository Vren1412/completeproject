from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from fastapi_backend import models
from fastapi_backend.database import engine, SessionLocal

# Initialize FastAPI app
app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Mount static files and set template directory
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------------
# ROUTES
# -----------------------------------

# GET: Login Page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# POST: Login Handler
@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    user_id: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.user_id == user_id,
        models.User.password == password
    ).first()
    if user:
        return RedirectResponse(url=f"/dashboard/{user.id}", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid credentials"})

# GET: Register Page
@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# POST: Register Handler
@app.post("/register")
def register(
    user_id: str = Form(...),
    name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": {}, "msg": "User already exists"})

    user = models.User(user_id=user_id, name=name, password=password, preferences="")
    db.add(user)
    db.commit()
    return RedirectResponse(url="/", status_code=302)

# GET: Dashboard
@app.get("/dashboard/{user_id}", response_class=HTMLResponse)
def dashboard(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

# POST: Update Dashboard Info
@app.post("/update_dashboard/{user_id}")
def update_dashboard(
    user_id: int,
    user_id_form: str = Form(...),
    name: str = Form(...),
    password: str = Form(...),
    course_interest: List[str] = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.user_id = user_id_form
    user.name = name
    user.password = password
    user.preferences = ",".join(course_interest)
    db.commit()
    return RedirectResponse(url=f"/dashboard/{user_id}", status_code=302)

# POST: Update only user_id (if needed)
@app.post("/update_userid/{user_id}")
def update_user_id(
    user_id: int,
    user_id_form: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.user_id = user_id_form
        db.commit()
    return RedirectResponse(url=f"/dashboard/{user_id}", status_code=302)