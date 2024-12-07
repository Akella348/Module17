from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated, List
from app.models.user import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]) -> List[User]:
    users = db.execute(select(User)).scalars().all()
    return users


@router.get("/{user_id}")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]) -> User:
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user


@router.post("/create")
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]) -> dict:
    db_user = User(user.dict(), slug=slugify(user.username))
    db.execute(insert(User).values(db_user.__dict__))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update/{user_id}")
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]) -> dict:
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    update_query = update(User).where(User.id == user_id).values(user.dict())
    db.execute(update_query)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]) -> dict:
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    delete_query = delete(User).where(User.id == user_id)
    db.execute(delete_query)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}