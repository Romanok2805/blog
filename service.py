
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import *


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return result.scalars().all()

async def get_user(session: AsyncSession, user_id: int) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def add_user(session: AsyncSession, name: str, age: int, forceId: int|None = None):
    # check forceId if free or not
    if forceId:
        user = await get_user(session, forceId)
        if user:
            return None
    new_user = User(name=name, age=age)
    if forceId:
        new_user.id = forceId
    session.add(new_user)
    await session.commit()
    return new_user

async def remove_user(session: AsyncSession, user_id: int):
    user = await get_user(session, user_id)
    if user:
        await session.execute(delete(Post).where(Post.user_id == user_id))
        await session.execute(delete(User).where(User.id == user_id))
        await session.commit()
        return user
    return None

async def edit_user(session: AsyncSession, user_id: int, name: str, age: int):
    user = await get_user(session, user_id)
    if user:
        await session.execute(update(User).where(User.id == user_id).values(name=name, age=age))
        await session.commit()
        return await get_user(session, user_id)
    return None

async def get_posts(session: AsyncSession) -> list[Post]:
    result = await session.execute(select(Post))
    return result.scalars().all()

async def get_post(session: AsyncSession, post_id: int) -> Post:
    result = await session.execute(select(Post).where(Post.id == post_id))
    return result.scalars().first()

async def add_post(session: AsyncSession, title: str, body: str, user_id: int):
    new_post = Post(title=title, body=body, user_id=user_id)
    session.add(new_post)
    return new_post

async def remove_post(session: AsyncSession, post_id: int):
    post = await get_post(session, post_id)
    if post:
        await session.execute(delete(Post).where(Post.id == post_id))
        await session.commit()
        return post
    return None

async def edit_post(session: AsyncSession, post_id: int, title: str, body: str, user_id: int):
    post = await get_post(session, post_id)
    if post:
        await session.execute(update(Post).where(Post.id == post_id).values(title=title, body=body, user_id=user_id))
        await session.commit()
        return await get_post(session, post_id)
    return None