from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import *
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])
Sess = Annotated[Session, Depends(get_db)]

@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users_query = db.scalars(select(User))
    return list(users_query.all())


@router.get('/user_id/{user_id}')
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_query = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    return user_query


@router.post('/create')
async def create_user(sess: Sess, user: CreateUser) -> dict:
    if sess.scalar(select(User.username)
                   .where(User.username == user.username)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Duplicated username')
    user_dict = dict(user)
    user_dict['slug'] = slugify(user.username)
    sess.execute(insert(User), user_dict)
    sess.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}

"""@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], new_user: CreateUser):
    result = db.execute(insert(User).values(username=new_user.username,
                                            firstname=new_user.firstname,
                                            lastname=new_user.lastname,
                                            age=new_user.age,
                                            slag=slugify(new_user.username)))
    db.commit()
    return {'status_code': 'status.HTTP_201_CREATED', 'transaction': 'Successful'}


   

    try:
        new_user_data = {
            "username": slugify(new_user.username),
            "firstname": new_user.firstname,
            "lastname": new_user.lastname,
            "age": new_user.age,
        }
        query = insert(User).values(**new_user_data)
        result = db.execute(query)
        db.commit()
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
    except Exception as e:
        # Обработка исключений, таких как уникальный ключ
        print(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create user due to: {e}",
        )
"""


@router.put('/update')
async def update_user(updated_user: UpdateUser, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_to_update = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    updated_user_data = updated_user.dict(exclude_unset=True)
    query = (
        update(User).
        where(User.id == user_id).
        values(**updated_user_data)
    )
    db.execute(query)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}



@router.delete('/delete')
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_to_delete = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    query = delete(User).where(User.id == user_id)
    db.execute(query)
    db.commit()
    return {"status_code": status.HTTP_204_NO_CONTENT, "transaction": "User deleted successfully!"}
