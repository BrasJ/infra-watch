from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth import get_password_hash

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def list_users(db: Session) -> List[User]:
    return db.query(User).all()

def create_user(db: Session, user_data: UserCreate) -> User:
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user_id: int, update_data: UserUpdate) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if update_data.password:
        user.hashed_password = get_password_hash(update_data.password)
    if update_data.email:
        user.email = update_data.email
    if update_data.username:
        user.username = update_data.username

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
