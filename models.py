from pydantic import BaseModel
from typing import Optional

class TodoItem(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class User(BaseModel):
    username: str

class UserCreate(User):
    password: str

class UserDB(User):
    hashed_password: str
