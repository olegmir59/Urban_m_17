from fastapi import FastAPI

from app import routers

app = FastAPI()

app.include_routers([routers])

app.add_api_route('/welcome', include_in_schema=False)({"message": "Welcome to Taskmanager"})


if __name__ == '__main__':
    print('PyCharm')
