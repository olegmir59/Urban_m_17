
from fastapi import APIRouter, Depends, status, HTTPException, FastAPI
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
# Функция создания slug-строки
from slugify import slugify
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
#   для delete
#from sqlalchemy.orm import Session
#from sqlalchemy.sql.expression import delete
#   для delete

from app.models import Task, User
from app.schemas import CreateUser, UpdateUser

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users_query = db.scalars(select(User))
    return list(users_query.all())


@router.get('/user_id/{user_id}')
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_query = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user_query is None:
        raise HTTPException(status_code=404, detail="User was not found")
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    return user_query


@router.get('/user_id/{user_id}/tasks')
async def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    tasks_query = db.execute(select(Task).where(Task.user_id == user_id))
    return list(tasks_query.scalars(Task))


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], new_user: CreateUser) -> dict:
    if db.scalar(select(User.username).where(User.username == new_user.username)):
        # Обработка исключений, таких как уникальный ключ
        raise HTTPException(status_code=409, detail='Duplicated username')
        #raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        #                    detail='Duplicated username')

    user_dict = dict(new_user)
    user_dict['slug'] = slugify(new_user.username)
    db.execute(insert(User), user_dict)
    db.commit()
    return {'status_code': 201, 'transaction': 'Successful'}
    #return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], updated_user: UpdateUser, user_id: int):
    user_to_update = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User was not found")
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    updated_user_data = updated_user.dict(exclude_unset=True)
    updated_user_data["slug"] = slugify(updated_user.username)
    query = (
        update(User).
        where(User.id == user_id).
        values(**updated_user_data)
    )
    db.execute(query)
    db.commit()
    return {"status_code": 200, "transaction": "User update is successful!"}

@router.delete('/delete')
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_to_delete = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User was not found")
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    query = delete(User).where(User.id == user_id)
    db.execute(query)
    db.commit()

    # Используем bulk_delete для удаления всех связанных записей Task
    query = delete(Task).where(Task.user_id == user_id)
    db.execute(query)
    db.commit()
    return {"status_code": 204, "transaction": "User deleted successfully!"}
    # return {"status_code": status.HTTP_204_NO_CONTENT, "transaction": "User deleted successfully!"}
