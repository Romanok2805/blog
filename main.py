import asyncio

import typer
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import service
from db.base import get_session, init_models

app = FastAPI()
cli = typer.Typer()

@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")

@app.get("/")
async def root():
    return {"docs": "http://10.10.0.201:8000/docs"}

class UserShema(BaseModel):
    userId: int|None = None
    name: str
    age: int

@app.get("/users", response_model=list[UserShema])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await service.get_users(session)
    return [UserShema(name=u.name, age=u.age, userId=u.id) for u in users]

@app.get("/users/{user_id}", response_model=UserShema)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await service.get_user(session, user_id)
    return UserShema(name=user.name, age=user.age, userId=user.id)

@app.post("/users", response_model=UserShema)
async def add_user(user: UserShema, session: AsyncSession = Depends(get_session)):
    user = await service.add_user(session, user.name, user.age, user.userId)
    if not user:
        raise HTTPException(status_code=403, detail="User already exist")
    try:
        await session.commit()
        return UserShema(name=user.name, age=user.age, userId=user.id)
    except Exception as ex:
        await session.rollback()
        return {"error": str(ex)}

@app.delete("/users/{user_id}", response_model=UserShema)
async def remove_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await service.remove_user(session, user_id)
    if not user:
        raise HTTPException(status_code=403, detail="User not found")
    
    return UserShema(name=user.name, age=user.age, userId=user.id)

@app.put("/users/{user_id}", response_model=UserShema)
async def update_user(
    user_id: int, user: UserShema, session: AsyncSession = Depends(get_session)
):
    user = await service.edit_user(session, user_id, user.name, user.age)
    try:
        await session.commit()
        return UserShema(userId=user.id, name=user.name, age=user.age)
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=403, detail=str(ex))

class PostShema(BaseModel):
    title: str
    body: str
    user_id: int

@app.get("/posts", response_model=list[PostShema])
async def get_posts(session: AsyncSession = Depends(get_session)):
    posts = await service.get_posts(session)
    return [PostShema(title=p.title, body=p.body, user_id=p.user_id) for p in posts]

@app.get("/posts/{post_id}", response_model=PostShema)
async def get_post(post_id: int, session: AsyncSession = Depends(get_session)):
    post = await service.get_post(session, post_id)
    return PostShema(title=post.title, body=post.body, user_id=post.user_id)

@app.post("/posts", response_model=PostShema)
async def add_post(post: PostShema, session: AsyncSession = Depends(get_session)):
    post = await service.add_post(session, post.title, post.body, post.user_id)
    try:
        await session.commit()
        return PostShema(title=post.title, body=post.body, user_id=post.user_id)
    except Exception as ex:
        await session.rollback()
        return {"error": str(ex)}

@app.delete("/posts/{post_id}", response_model=PostShema)
async def remove_post(post_id: int, session: AsyncSession = Depends(get_session)):
    post = await service.remove_post(session, post_id, post.title, post.body, post.user_id)
    if not post:
        raise HTTPException(status_code=403, detail="Post not found")
    try:
        await session.commit()
        return PostShema(title=post.title, body=post.body, user_id=post.user_id)
    except Exception as ex:
        await session.rollback()
        return {"error": str(ex)}
    
@app.put("/posts/{post_id}", response_model=PostShema)
async def update_post(
    post_id: int, post: PostShema, session: AsyncSession = Depends(get_session)
):
    post = await service.edit_post(session, post_id, post.title, post.body, post.user_id)
    if not post:
        raise HTTPException(status_code=403, detail="Post not found")
    try:
        await session.commit()
        return PostShema(title=post.title, body=post.body, user_id=post.user_id)
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=403, detail=str(ex))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)