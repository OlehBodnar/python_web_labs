from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from crud import create_user, get_user_by_username, verify_password
import schemas
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Підключення статичних файлів
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")
#templates = Jinja2Templates(directory="templates")


# Маршрути для рендерингу сторінок
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/products", response_class=HTMLResponse)
async def catalog_page(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse("admin-home.html", {"request": request})

@app.get("/user", response_class=HTMLResponse)
async def user_page(request: Request):
    return templates.TemplateResponse("user-home.html", {"request": request})

# Маршрут для реєстрації
@app.post("/register/")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Перевірка наявності користувача
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Користувач вже існує")
    # Створення нового користувача
    create_user(db=db, user=user)
    return {"message": "Реєстрація успішна"}

# Маршрут для логіну
@app.post("/login/")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Отримано запит на логін: {user.username}")

    db_user = get_user_by_username(db, user.username)
    if not db_user:
        logger.warning("Користувача не знайдено")
        raise HTTPException(status_code=400, detail="Неправильне ім'я користувача або пароль")

    if not verify_password(user.password, db_user.hashed_password):
        logger.warning("Пароль невірний")
        raise HTTPException(status_code=400, detail="Неправильне ім'я користувача або пароль")

    logger.info("Успішний вхід")
    return {"role": "admin" if db_user.is_admin else "user"}


