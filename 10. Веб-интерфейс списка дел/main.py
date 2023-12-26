from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

tasks = [
    {"id": 1, "description": "Купить молоко", "done": False},
    {"id": 2, "description": "Погулять с собакой", "done": True},
]

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})


@app.post("/add-task/")
async def add_task(description: str = Form(...)):
    new_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    new_task = {"id": new_id, "description": description, "done": False}
    tasks.append(new_task)
    return RedirectResponse(url="/", status_code=303)

@app.post("/update-task/")
async def update_task(task_id: int = Form(...)):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            return RedirectResponse(url="/", status_code=303)
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete-task/")
async def delete_task(task_id: int = Form(...)):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[index]
            return RedirectResponse(url="/", status_code=303)
    return RedirectResponse(url="/", status_code=303)
