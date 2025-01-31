from fastapi import FastAPI
from app.routers import task
from app.routers import user
from app.backend.db import engine, Base
import uvicorn

app = FastAPI()

@app.get("/")
async def welcome():
    return {"message":  "Welcome to Taskmanager"}


# Подключаем роутеры
app.include_router(user.router)
app.include_router(task.router)

# Создаём таблицы в базе данных
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
