
"""
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///./taskmanager.db', echo=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./taskmanager.db"  # Путь к базе данных SQLite
# Создаём движок для подключения к базе данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Создаём фабрику сессий для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()
