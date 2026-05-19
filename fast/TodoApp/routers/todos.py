
from fastapi import APIRouter, Depends, HTTPException,Path
from database import SessionLocal
from model import Todo
from typing import Annotated
from sqlalchemy.orm import Session

from starlette import status
from pydantic import BaseModel,Field



router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

class TodoCreate(BaseModel):
    title: str = Field(min_length=3)
    priorty: int = Field(gt=0)
    description: str = Field(min_length=5, max_length=100)
    complete: bool 

    
@router.get('/get_all info',status_code= status.HTTP_200_OK)
def get_all_info(db:db_dependency):
    return db.query(Todo).all()
@router.get('/get_info/{id}',status_code= status.HTTP_200_OK)
def get_info(db:db_dependency,id:int = Path(gt=0)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
@router.post('/add_info')
def add_info(db:db_dependency, todo:TodoCreate):

    db_todo = Todo(**todo.dict())

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo
@router.put('/update_info/{id}')
def update_info(db:db_dependency, todo_model:TodoCreate, id:int = Path(gt=0)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    for key, value in todo_model.dict().items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo
@router.delete('/erase/{id}')
def delet_entry(db:db_dependency , id : int = Path(gt=0)):
    todo_enetry = db.query(Todo).filter(Todo.id == id).first()
    if not todo_enetry:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_enetry)
    db.commit()
    
    return {"message": "Todo entry deleted successfully"}