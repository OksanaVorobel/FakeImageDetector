from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.hash import bcrypt
from starlette import status
import jwt

from app.core.config import app_config
from app.db.models import User
from app.services.users import UsersService
from app.repositories.dependencies import users_service


class AuthService:
    SECRET_KEY = app_config.secret_key
    JWT_ALGORITHM = app_config.hash_algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/sign_in")

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.verify(password, hashed_password)

    def encode_token(self, payload: dict, exp: int = None) -> str:
        if exp:
            payload["exp"] = datetime.utcnow() + timedelta(minutes=exp)

        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.JWT_ALGORITHM)

    def decode_token(self, encoded_token: str) -> Optional[dict]:
        try:
            decoded_token = jwt.decode(
                encoded_token, self.SECRET_KEY, algorithms=[self.JWT_ALGORITHM]
            )
            return decoded_token
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            return None

    async def get_current_user(
            self, token: str = Depends(oauth2_scheme),
            users_service: UsersService = Depends(users_service)
    ) -> User:
        decoded_token = self.decode_token(token)
        if not decoded_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        user = await users_service.find_user_by_email(decoded_token.get("sub"))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user

    def create_tokens(self, email: str) -> dict:
        access_token = self.encode_token(
            payload={"sub": email}, exp=app_config.access_token_expire_minutes
        )
        refresh_token = self.encode_token(
            payload={"sub": email}, exp=app_config.refresh_token_expire_minutes
        )
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def sign_in(
            self, data: OAuth2PasswordRequestForm = Depends(),
            users_service: UsersService = Depends(users_service)
    ) -> dict:
        user = await users_service.find_user_by_email(data.username)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        if not self.verify_password(data.password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        return {"user_id": user.id, **self.create_tokens(user.email)}


auth_service = AuthService()
