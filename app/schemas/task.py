from pydantic import BaseModel

# по лекции /рабочий вариант, только еще slug запрашивает/


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


