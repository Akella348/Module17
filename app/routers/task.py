from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from app.models.user import User
from app.models.task import Task
from app.backend.db_depends import get_db
from schemas import CreateTask, UpdateTask, TaskResponse

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/", response_model=List[TaskResponse])
async def all_tasks(db: Session = Depends(get_db)) -> List[TaskResponse]:
    tasks = db.execute(select(Task)).scalars().all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def task_by_id(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    return task

@router.post("/create", response_model=dict)
async def create_task(task: CreateTask, user_id: int, db: Session = Depends(get_db)) -> dict:
    db_task = Task(
        title=task.title,
        content=task.content,
        priority=task.priority,
        user_id=user_id,
        slug=slugify(task.title)
    )
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    else:
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/{task_id}/update", response_model=TaskResponse)
async def update_task(task_id: int, task: UpdateTask, db: Session = Depends(get_db)) -> TaskResponse:
    db_task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    update_query = update(Task).where(Task.id == task_id).values(**task.dict())
    db.execute(update_query)
    db.commit()
    return db_task

@router.delete("/{task_id}", response_model=dict)
async def delete_task(task_id: int, db: Session = Depends(get_db)) -> dict:
    db_task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task deletion is successful!'}