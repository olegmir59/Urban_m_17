from pydantic import BaseModel

"""
class User(BaseModel):
    id: int  #  Поле для уникального идентификатора
    username: str 
    firstname: str
    lastname: str
    age: int

#    class Config:
#        orm_mode = True # Указывает, что объект может быть преобразован из ORM (например, SQLAlchemy)
"""


class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int


class CreateTask(BaseModel):
    title: str
    content: str
    priority: int


class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int
