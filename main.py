from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from models import TodoItem, UserDB
from security import create_access_token, get_current_user

app = FastAPI()

# In-memory database (for demonstration purposes)
db = []

# Security
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# CRUD
@app.post("/todos/", response_model=TodoItem)
async def create_todo(todo: TodoItem, current_user: str = Depends(get_current_user)):
    db.append({"title": todo.title, "description": todo.description, "completed": todo.completed, "user": current_user})
    return todo

@app.get("/todos/", response_model=List[TodoItem])
async def read_todos(skip: int = 0, limit: int = 10, current_user: str = Depends(get_current_user)):
    user_todos = [todo for todo in db if todo["user"] == current_user]
    return user_todos[skip : skip + limit]

@app.get("/todos/{todo_id}", response_model=TodoItem)
async def read_todo(todo_id: int, current_user: str = Depends(get_current_user)):
    todo = next((t for t in db if t["user"] == current_user and t.get("id") == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, todo: TodoItem, current_user: str = Depends(get_current_user)):
    todo_index = next((i for i, t in enumerate(db) if t["user"] == current_user and t.get("id") == todo_id), None)
    if todo_index is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db[todo_index] = {"id": todo_id, "title": todo.title, "description": todo.description, "completed": todo.completed, "user": current_user}
    return db[todo_index]

@app.delete("/todos/{todo_id}", response_model=TodoItem)
async def delete_todo(todo_id: int, current_user: str = Depends(get_current_user)):
    todo_index = next((i for i, t in enumerate(db) if t["user"] == current_user and t.get("id") == todo_id), None)
    if todo_index is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    deleted_todo = db.pop(todo_index)
    return deleted_todo

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

