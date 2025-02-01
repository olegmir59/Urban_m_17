
from fastapi import APIRouter, Depends, status, HTTPException, FastAPI
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
# Функция создания slug-строки
from slugify import slugify
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete


from app.models import *
from app.schemas import CreateTask, UpdateTask

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    task_query = db.scalars(select(Task))
    return list(task_query.all())


@router.get('/task_id/{task_id}')
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task_query = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task_query is None:
         raise HTTPException(status_code=404, detail="User was not found")
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
    return task_query


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], new_task: CreateTask):
    new_task_data = {
        "title": new_task.title,
        "content": new_task.content,
        "priority": new_task.priority,
        "user_id": new_task.user_id,                  # user, а не user_id
        "slug": slugify(new_task.title)
    }
    query = insert(Task).values(**new_task_data)
    db.execute(query)
    db.commit()
    return {"status_code": 201, "transaction": "Successful"}
    #return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_task(new_task: UpdateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_to_update = db.execute(select(Task).where(Task.id == user_id)).scalar_one_or_none()
    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User was not found")

    updated_task_data = update_task.dict(exclude_unset=True)
    query = (
        update(Task).
        where(Task.id == user_id).
        values(**updated_task_data)
    )
    db.execute(query)
    db.commit()
    return {"status_code": 200, "transaction": "Task update is successful!"}


@router.delete("/delete")
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task_to_delete = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task_to_delete is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    query = delete(Task).where(Task.id == task_id)
    db.execute(query)
    db.commit()
    return {"status_code": 200, "transaction": "Task deleted successfully!"}
