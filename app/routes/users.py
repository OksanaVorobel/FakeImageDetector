from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.db.models import User
from app.schemas.users import SignUpRequest, AuthRequest, UserDetails
from app.services.auth import auth_service
from app.services.users import UsersService
from app.repositories.dependencies import users_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/sign_up", response_model=AuthRequest, status_code=status.HTTP_200_OK)
async def sign_up(
        data: SignUpRequest,
        service: UsersService = Depends(users_service)
):
    data.password = auth_service.hash_password(data.password)
    user_id = await service.add_user(data)
    return {"user_id": user_id, **auth_service.create_tokens(data.email)}


@router.post("/sign_in", response_model=AuthRequest, status_code=status.HTTP_200_OK)
async def sign_in(
        data: OAuth2PasswordRequestForm = Depends(),
        service: UsersService = Depends(users_service)
):
    return await auth_service.sign_in(data, service)


@router.get("/me", response_model=UserDetails, status_code=status.HTTP_200_OK)
async def get_my_profile(
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
