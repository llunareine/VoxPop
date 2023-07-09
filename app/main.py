from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
import datetime
from .repository import CommentsRepository

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
repository = CommentsRepository()

@app.get("/")
def read_index(request: Request):
    comments = repository.get_all()

    return comments

@app.get("/comments")
def get_comments(request: Request, page: int = 1, page_size: int = CommentsRepository):
    comments = repository.get_all()
    current_time = datetime.datetime.now()
    sorted_comments = sorted(comments, key=lambda x: abs(current_time - x["date"]))
    start = (page - 1) * page_size
    end = start + page_size
    return sorted_comments[start:end]

@app.get ("/comments/new/")
def read_comments(request: Request):
    return {"request": request}

@app.post("/comments/new/")
def add_comments(name: str = Form(),comment: str = Form(), category: str = Form()):
    comment = {
        "name": name,
        "comment": comment,
        "category": category,
        "date": datetime.datetime.now()
    }
    repository.save(comment)
    return comment

