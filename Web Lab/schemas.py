from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool = False  # Додаємо роль під час реєстрації

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    email: str
    is_admin: bool = False

    class Config:
       from_attributes = True
