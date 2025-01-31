from pydantic import BaseModel

# по лекции

class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int
    slug: str


class CreateUser(UserBase):
    pass
#    username: str
#    firstname: str
#    lastname: str
#    age: int


class UpdateUser(UserBase):
    pass
#    firstname: str
#    lastname: str
#    age: int


class User(UserBase):
    id: int

    class Config:
        orm_mode = True  # Позволяет работать с данными ORM


class TaskBase(BaseModel):
    title: str
    content: str
    priority: int
    completed: bool
    user_id: int
    slug: str


class CreateTask(TaskBase):
    pass
#    title: str
#    content: str
#    priority: int


class UpdateTask(TaskBase):
    pass
#    title: str
#    content: str
#    priority: int


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True  # Позволяет работать с данными ORM


"""   более простой вариант

class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

class UpdateUser (BaseModel):
    firstname: str
    lastname: str
    age: int

class CreateTask (BaseModel):
    title: str
    content: str
    priority: int

class UpdateTask (BaseModel):
    title: str
    content: str
    priority: int 
    
"""