from typing import Type

from fastapi import HTTPException
from starlette import status

from app.schemas.users import SignUpRequest
from app.utils.repository import AbstractRepository


class UsersService:
    def __init__(self, users_repo: Type[AbstractRepository]):
        self.users_repo: AbstractRepository = users_repo()

    async def add_user(self, user: SignUpRequest):
        email = await self.find_user_by_email(user.email)
        if email is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return await self.users_repo.add_one(user.model_dump())

    async def get_users(self, limit: int, offset: int):
        return await self.users_repo.find_all(limit, offset)

    async def get_user_by_id(self, user_id: int):
        user = await self.users_repo.find_by_filter({"id": user_id})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    async def delete_user(self, user_id: int, current_user_id: int):
        user = await self.users_repo.find_by_filter({"id": user_id})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if current_user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        await self.users_repo.delete_by_id(user_id)

    async def find_user_by_email(self, email: str):
        return await self.users_repo.find_by_filter({"email": email})
