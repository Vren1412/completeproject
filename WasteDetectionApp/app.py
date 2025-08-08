from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi import UploadFile, File
import shutil
import os
from utils import detect_waste

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='your_secret_key')

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin123":
        request.session['user'] = username
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(request: Request):
    if 'user' not in request.session:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("dashboard.html", {"request": request, "message": ""})

@app.post("/upload", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    if 'user' not in request.session:
        return RedirectResponse(url="/", status_code=302)

    contents = await file.read()
    file_path = os.path.join("static/uploads", file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    request.session['uploaded_file'] = file_path
    return templates.TemplateResponse("dashboard.html", {"request": request, "message": "Image uploaded successfully!"})

@app.post("/predict", response_class=HTMLResponse)
def predict_image(request: Request):
    if 'user' not in request.session:
        return RedirectResponse(url="/", status_code=302)

    image_path = request.session.get('uploaded_file')
    if not image_path or not os.path.exists(image_path):
        return templates.TemplateResponse("dashboard.html", {"request": request, "message": "Please upload an image first."})

    result_path, label = detect_waste(image_path)
    return templates.TemplateResponse("result.html", {"request": request, "result_path": result_path, "label": label})
