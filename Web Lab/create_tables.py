from sqlalchemy import create_engine
from database import Base
from models import User  # Імпортуйте вашу модель User

# Ваша база даних
SQLALCHEMY_DATABASE_URL = "sqlite:///./user.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Створення таблиць
Base.metadata.create_all(bind=engine)
