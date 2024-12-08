from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    age: int
    slug: str

    class Config:
        orm_mode = True

class TaskResponse(BaseModel):
    id: int
    title: str
    content: str
    priority: int
    completed: bool
    user_id: int
    slug: str

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int

class CreateTask(BaseModel):
    title: str
    content: str
    priority: int

class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int