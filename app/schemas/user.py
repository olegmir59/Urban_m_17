from pydantic import BaseModel


# по лекции /рабочий вариант, только еще slug запрашивает/

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
