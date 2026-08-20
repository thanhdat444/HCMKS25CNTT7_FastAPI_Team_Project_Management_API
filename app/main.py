from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.db.database import Base, engine
from app.models import project, project_members, task, user

app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "error": {
                "code": exc.status_code,
                "path": request.url.path
            }
        }
    )

@app.get("/")
def root():
    return {"message": "Chào mừng đến với API Authentication Demo. Hãy truy cập /docs để test."}

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }