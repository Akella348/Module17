from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from app.models.user import User
from app.backend.db_depends import get_db
from schemas import CreateUser, UpdateUser, UserResponse

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/", response_model=List[UserResponse])
async def all_users(db: Session = Depends(get_db)) -> List[UserResponse]:
    users = db.execute(select(User)).scalars().all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def user_by_id(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user

@router.post("/create", response_model=UserResponse)
async def create_user(user: CreateUser, db: Session = Depends(get_db)) -> UserResponse:
    db_user = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slugify(user.username)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_id}/update", response_model=UserResponse)
async def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    update_query = update(User).where(User.id == user_id).values(**user.dict())
    db.execute(update_query)
    db.commit()
    return db_user

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> dict:
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}
