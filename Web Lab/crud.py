from models import User
from schemas import UserCreate
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import logging

# Setting up password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Setting up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_password_hash(password: str) -> str:
    """Hash the password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: UserCreate, is_admin:bool = False) -> User:
    """Create a new user in the database."""
    logger.info(f"Creating user: {user.username}")
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_admin = is_admin

    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created successfully: {user.username}")
    return db_user

def get_user_by_username(db: Session, username: str) -> User:
    """Get a user by username."""
    logger.info(f"Fetching user by username: {username}")
    return db.query(User).filter(User.username == username).first()
