from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import project, project_members, task, user

app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.get("/")
def root():
    return {"message": "Chào mừng đến với API Authentication Demo. Hãy truy cập /docs để test."}