from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from typing import List
from pydantic import BaseModel

import logging
import time
import os

#uvicorn todo:app --reload 
#.venv\Scripts\activate
#curl -X POST "http://127.0.0.1:8000/tasks" -H "Content-Type: application/json" -d "[{\"task\": \"Дописать код для упражнения 1.2\",\"status\": false},{\"task\": \"сходить покушать\", \"status\": false}]"

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@host.docker.internal:5432/todo_list"

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

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file_name = os.path.join(log_dir, f'app_logs_{time.strftime("%Y-%m-%d_%H-%M-%S")}.log')

log_format = '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - | %(elapsed_time).2f | %(http_method)s | %(url)s |\n| %(status_code)s |'

formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler(log_file_name)
file_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()

    elapsed_time = end_time - start_time
    log_context = {
        'elapsed_time': elapsed_time,
        'http_method': request.method,
        'url': request.url.path,
        'status_code': response.status_code
    }
    
    logger.info("", extra=log_context)
    return response

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

def int_to_roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]
    syms = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]
    roman_num = ""
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syms[i]
            num -= val[i]
        i += 1
    return roman_num

@app.post("/int_to_roman")
def convert_to_roman(data: dict):
    number = data.get("number")
    if number is None or not isinstance(number, int):
        return JSONResponse(status_code=424, content={"message": "Invalid data"})
    if number <= 0 or number > 3999:
        return JSONResponse(status_code=424, content={"message": "Please provide a number between 1 and 3999"})
    roman_number = int_to_roman(number)
    return JSONResponse(status_code=200, content={"message": roman_number})