from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from typing import List
from pydantic import BaseModel

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost:5432/todo_list"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)
    status = Column(Boolean)

class TaskModel(BaseModel):
    task: str
    status: bool

#Base.metadata.create_all(bind=engine)

#получение задачи по id
@app.get("/tasks/{task_id}")
def get_tasks(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return JSONResponse(status_code=424, content={"message": "Status code 424"})
    db = SessionLocal()
    result = db.query(Task).filter(Task.task_id == task_id).first()
    if result == None:
        db.close()
        return JSONResponse(status_code=404, content={"message": "Status code 404 : task not found"})
    else:
        db.close()
    return JSONResponse(status_code=200, content={"message": ["Status code 200", jsonable_encoder(result)]})

#добавление новой задачи
@app.post("/tasks")
def add_task(tasks: List[dict]):
    db = SessionLocal()
    for task_data in tasks:
        try:
            validator = TaskModel(task=task_data['task'], status=task_data['status'])
            new_task = Task(task=task_data['task'], status=task_data['status'])
        except Exception as e:
            db.close()
            return JSONResponse(status_code=422, content={"message": "Status code 422"})
        db.add(new_task)
    db.commit()
    db.close()
    return JSONResponse(status_code=200, content={"message": ["Status code 200", tasks]})


#обновление задачи
@app.put("/tasks/{task_id}")
def update_task(task_id: int, tasks: dict):
    db = SessionLocal()
    try:
        validator = TaskModel(task_id = task_id, task=tasks["task"], status=tasks["status"])
    except Exception as e:
        db.close()
        return JSONResponse(status_code=424, content={"message": "Status code 424"})
    result = db.query(Task).filter(Task.task_id == task_id).update({Task.task: tasks["task"], Task.status: tasks["status"]})
    if result == 0:
        db.close()
        return JSONResponse(status_code=422, content={"message": "Status code 422 : task not found"})
    else:
        db.commit()
        db.close()
    return JSONResponse(status_code=200, content={"message": ["Status code 200", tasks]})

#удаление задачи
@app.delete("/tasks/{task_id}")
def delete_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return JSONResponse(status_code=424, content={"message": "Status code 424"})
    
    db = SessionLocal()
    result = db.query(Task).filter(Task.task_id == task_id).delete()
    if result == 0:
        db.close()
        return JSONResponse(status_code=404, content={"message": "Status code 404 : task not found"})
    else:
        db.commit()
        db.close()
    return JSONResponse(status_code=200, content={"message": "Status code 200"})