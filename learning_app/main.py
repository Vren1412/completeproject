from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
app = FastAPI()
# Create the database tables
models.Base.metadata.create_all(bind=engine)
# Templating and static file configuration
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Route: Login Page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
# Route: Login Handler
@app.post("/login", response_class=HTMLResponse)
def login(request: Request, user_id: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id, models.User.password == password).first()
    if user:
        return RedirectResponse(url=f"/dashboard/{user.id}", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid credentials"})
# Route: Registration Page
@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
# Route: Registration Handler
@app.post("/register")
def register(user_id: str = Form(...), name: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = models.User(user_id=user_id, name=name, password=password, course_interest="")
    db.add(user)
    db.commit()
    return RedirectResponse(url="/", status_code=302)
# Route: Dashboard Page
@app.get("/dashboard/{user_id}", response_class=HTMLResponse)
def dashboard(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})
# Route: Dashboard Update Handler
@app.post("/update_dashboard/{user_id}")
def update_dashboard(user_id: int, name: str = Form(...), password: str = Form(...), course_interest: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.name = name
    user.password = password
    user.course_interest = course_interest
    db.commit()
    return RedirectResponse(url=f"/dashboard/{user_id}", status_code=302)
