from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from users.auth import SECRET_KEY
import jwt
from pathlib import Path
import requests

API_URL = "http://localhost:8000/api"

app = FastAPI()

base_dir = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(base_dir / "templates"))
app.mount("/static", StaticFiles(directory=str(base_dir / "static")), name="static")


def get_username_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")  # sub — это имя пользователя в токене
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return None

@app.get("/")
def index(request: Request):
    try:
        response = requests.get(f"{API_URL}/blogs")
    except ConnectionError as e:
        raise (e)
    blogs = response.json()
    token = request.cookies.get("token")  # Получаем токен из куков
    username = get_username_from_token(token) if token else None
    return templates.TemplateResponse(
        name="index.html",
        context=
            {
                "request": request, 
                "blogs": blogs,
                "username": username
            }
        )


@app.get("/blogs")
def detail(request: Request, blog_id: int):
    response = requests.get(f"{API_URL}/blogs/{blog_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=response.status_code)
    blog = response.json()
    token = request.cookies.get("token")  # Получаем токен из куков
    username = get_username_from_token(token) if token else None  
    return templates.TemplateResponse("detail.html",
            {
                "request": request,
                "blog": blog,
                "username": username
            }
        )   

# Страница создания новой записи
@app.get("/blogs/new")
async def create_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/blogs/new")
async def create_blog(title: str = Form(...), content: str = Form(...)):
    data = {"article_title": title, "content": content}
    response = requests.post(f"{API_URL}/blogs", json=data)
    if response.status_code == 201:
        return RedirectResponse(url="/", status_code=303)
    else:
        raise HTTPException(status_code=500, detail="Error creating blog")
    
    return RedirectResponse(url="/", status_code=303)

    

@app.get("/blogs/edit/")
def edit_form(request: Request, blog_id: int):
    response = requests.get(f"{API_URL}/blogs/{blog_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404)
    else:
        blog = response.json()
        return templates.TemplateResponse("form.html", 
                                    {
                                        "request": request,
                                        "blog": blog     
                                    }
                                )

@app.post("/blogs/edit/")
def edit_blog(
        blog_id: int,
        title: str = Form(...),
        content: str = Form(...)
    ):

    data = {
        "article_title": title,
        "content": content
    }

    response = requests.patch(f"{API_URL}/blogs/{blog_id}", json=data)

    if response.status_code == 200:
        return RedirectResponse(url=f"/blogs/?blog_id={blog_id}", status_code=303)
    else:
        raise HTTPException(status_code=500)
    
@app.post("/blogs/delete/")
def delete_blog(blog_id: int):
    response = requests.delete(f"{API_URL}/blogs/{blog_id}")
    if response.status_code == 200:
        return RedirectResponse("/", status_code=303)
    else:
        raise HTTPException(status_code=500)
    
# Страница входа
@app.get("/login"   )
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
