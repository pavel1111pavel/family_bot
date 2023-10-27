from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

DATABASE_URL = "sqlite:///DB.db"  # Используйте свой URL базы данных

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Определите отношение между категорией и задачей, если требуется
    tasks = relationship("Task", back_populates="category")

    def get_tasks(self, db: Session):
        return db.query(Task).filter(Task.category_id == self.id).all()

    def get_category(self, db: Session, obj):
        return db.query(Task).filter(obj.category_id == self.id)
    @classmethod
    def create_category(cls, db: Session, name: str):
        new_category = cls(name=name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    task_text = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)



    # Добавьте следующую строку для связи с категорией
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="tasks")

class UserResponse(Base):
    __tablename__ = 'user_responses'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    response_text = Column(String)
    created_at = Column(DateTime, default=func.now())


# Создание таблиц в базе данных
def create_tables():
    Base.metadata.create_all(bind=engine)
