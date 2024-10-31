from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import User
from crud import get_user_by_username
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
