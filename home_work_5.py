from fastapi import FastAPI, status, Body, HTTPException, Request, Form, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates


app = FastAPI() # Start - uvicorn home_work_5:app
templates = Jinja2Templates(directory="hw_5_templates")

users_db = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users":users_db})


@app.get('/user/{user_id}')
def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user":users_db[user_id - 1]})
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post('/users/{username}/{age}')
async def add_users(username: str =
                    Path(min_length=5, max_length=20, description="Enter your name", example="Mihail")
                        , age: int =
                    Path(ge=18, le=120, description='Enter age',example=24)) -> User:
    user = User(id=len(users_db)+1, username=username, age=age)
    users_db.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def put_users(user_id: int =
                    Path(ge=1, le=100, description='Enter User ID', example=1)
                , username: str =
                    Path(min_length=5, max_length=20, description='Enter username',example='UrbanUser')
                      , age: int =
                    Path(ge=18, le=120, description='Enter age',example=24)) -> User:

        for user in users_db:
            if user.id == user_id:
                user.username = username
                user.age = age
                return user
        raise HTTPException(status_code=404, detail="User was not found")




@app.delete('/user/{user_id}')
async def del_users(user_id: int = Path(ge=1, le=100, description='Enter User ID', example=1)) -> User:
    for user in users:
        if user.id == user_id:
            return users.pop(users.index(user))
    raise HTTPException(status_code=404, detail="User was not found")
