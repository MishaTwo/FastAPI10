from typing import List
from fastapi import FastAPI, HTTPException
from schema import ToDoCreate, ToDoUpdate, ToDoResponse
from database.base import session
from database.base import create_db
from database.todo import ToDo

app = FastAPI()

create_db()

@app.post("/todos/", response_model=ToDoResponse)
async def create_task(todo: ToDoCreate):
    db_todo = ToDo()
    session.add(db_todo)
    session.commit()
    return db_todo


@app.get("/todos/", response_model=List[ToDoResponse])
async def get_tasks():
    all_tasks = session.query(ToDo).all()
    return all_tasks

@app.get("/todos/{todo_id}", response_model=ToDoResponse)
async def get_task_by_id(todo_id: int):
    todo = session.query(ToDo).filter(ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return todo

@app.put("/todos/{todo_id}/", response_model=ToDoResponse)
def update_todo(todo_id: int, todo: ToDoUpdate):
    todo_obj = session.query(ToDo).filter(ToDo.id == todo_id).first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in todo.dict().items():
        setattr(todo_obj, key, value)
    session.commit()
    session.refresh(todo)
    return todo_obj


@app.delete("/todos/{todo_id}")
async def delete_task(todo_id: int):
    todo_obj = session.query(ToDo).filter(ToDo.id == todo_id).first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(todo_obj)
    session.commit()
    return {"detail": "Todo was deleted successfully"}

@app.get('/todos/completed/', response_model=List[ToDoResponse])
async def completed_task():
    tasks = session.query(ToDo).filter_by(completed=True)
    return tasks

@app.get('/todos/completed/', response_model=List[ToDoResponse])
async def completed_task():
    tasks = session.query(ToDo).filter_by(completed=True)
    return tasks

@app.get('/todos/uncompleted/', response_model=List[ToDoResponse])
async def uncompleted_task():
    tasks = session.query(ToDo).filter_by(completed=False)
    return tasks

@app.patch('/tasks/{id}/uncomplete/', response_model=ToDoResponse) 
async def uncomplete_tasks(id: int):
    task = session.query(ToDo).get(id)
    if task:
        task.completed = False
        session.commit()
    return task
        