from database import engine
from fastapi import FastAPI
import model

from routers import auth, todos



app = FastAPI()
model.base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)