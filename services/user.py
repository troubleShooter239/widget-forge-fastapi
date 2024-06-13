from typing import Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.db_init import db_dependency


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def authenticate(
            self, email: str, hashed_password: str
    ) -> User | None:
        user = (
            await self.db_session.execute(
                select(User).where(User.email == email)
            )
        ).scalar_one_or_none()
        if user is None:
            return None

        return user if user.hashed_password == hashed_password else None

    async def create_user(
        self, email: str, hashed_password: str, widgets: str,
    ) -> User:
        new_user = User(
            email=email, hashed_password=hashed_password, widgets=widgets
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: int) -> int | None:
        res = await self.db_session.execute(
            update(User).where(User.id == user_id).returning(User.id)
        )
        user_id_row = res.fetchone()
        return user_id_row[0] if user_id_row is not None else None
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        res = await self.db_session.execute(
            select(User).where(User.id == user_id)
        )
        user_row = res.fetchone()
        return user_row[0] if user_row is not None else None

    async def get_user_by_email(self, email: str) -> User | None:
        res = await self.db_session.execute(
            select(User).where(User.email == email)
        )
        user_row = res.fetchone()
        return user_row[0] if user_row is not None else None

    async def update_user(self, user_id: int, **kwargs) -> int | None:
        res = await self.db_session.execute(
            update(User)
            .where(User.id == user_id)
            .values(kwargs)
            .returning(User.id)
        )
        user_id_row = res.fetchone()
        return user_id_row[0] if user_id_row is not None else None
    

def get_user_service(db: db_dependency) -> UserService:
    return UserService(db)

user_service_dependency = Annotated[UserService, Depends(get_user_service)]