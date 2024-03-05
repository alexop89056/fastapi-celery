from fastapi import FastAPI
from app.routes import user_router, auth_router, task_router
from app.models import db, User, Task
from app.config import ROOT_PATH

app = FastAPI(root_path=ROOT_PATH)

# Connect to the database and create tables
db.connect()
db.create_tables([User, Task])

# Include routers
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(task_router)
