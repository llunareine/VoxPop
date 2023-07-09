from fastapi import FastAPI, Form, Request
import datetime
from fastapi.responses import RedirectResponse
from .repository import CommentsRepository
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

repository = CommentsRepository()
app.mount("/static", StaticFiles(directory="static"), name='static')

templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_index(request: Request, page: int = 1, page_size: int = 5):
    comments = repository.get_all()
    total_comments = len(comments)
    max_page = (total_comments - 1) // page_size + 1

    start = (page - 1) * page_size
    end = start + page_size
    paginated_comments = comments[start:end]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "comments": paginated_comments,
            "page": page,
            "page_size": page_size,
            "total_comments": total_comments,
            "max_page": max_page,
        },
    )


@app.post("/comments/new/")
def add_comments(request:Request,name: str = Form(...), comment: str = Form(...), category: str = Form(...)):
    comment_data = {
        "name": name,
        "comment": comment,
        "category": category,
        "date": datetime.datetime.now()
    }
    repository.save(comment_data)
    return RedirectResponse("/",status_code=303)




