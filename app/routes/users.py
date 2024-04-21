from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.db.models import User
from app.schemas.users import SignUpRequest, AuthRequest, UserDetails
from app.services.auth import auth_service
from app.services.users import UsersService
from app.repositories.dependencies import users_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/sing_up", response_model=AuthRequest, status_code=status.HTTP_201_CREATED)
async def sing_up(
        data: SignUpRequest,
        service: UsersService = Depends(users_service)
):
    data.password = auth_service.get_password_hash(data.password)
    user = await service.add_user(data)
    return f"User id:{user}"


@router.post("/sing_in", response_model=AuthRequest, status_code=status.HTTP_200_OK)
async def sing_in(
        data: OAuth2PasswordRequestForm = Depends(),
        service: UsersService = Depends(users_service)
):
    return await auth_service.sing_in(data, service)


@router.post("/me", response_model=UserDetails, status_code=status.HTTP_200_OK)
async def sing_in(
        current_user: User = Depends(auth_service.get_current_user)
):
    return current_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        service: UsersService = Depends(users_service),
        current_user: User = Depends(auth_service.get_current_user)
):
    await service.delete_user(user_id, current_user.id)
