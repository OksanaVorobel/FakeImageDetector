import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class FastAPIConfig(BaseSettings):
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = os.getenv("PORT", 8000)

    db_user: str = os.getenv("POSTGRES_USER")
    db_password: str = os.getenv("POSTGRES_PASSWORD")
    db_name: str = os.getenv("POSTGRES_DB")
    db_port: int = os.getenv("POSTGRES_PORT")

    secret_key: str = os.getenv("SECRET_KEY")
    hash_algorithm: str = os.getenv("ALGORITHM", "HS256")
    secret_auth_key: str = os.getenv("SECRET_AUTH_KEY")
    access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    refresh_token_expire_minutes: int = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 10080)


class CNNModelConfig(BaseSettings):
    epochs: int = os.getenv("EPOCHS", 25)
    batch_size: int = os.getenv("BATCH_SIZE", 48)
    img_height: int = os.getenv("IMG_HEIGHT", 128)
    img_width: int = os.getenv("IMG_WIDTH", 128)
    model_file_name: str = os.getenv("MODEL_FILE_NAME", "model_new_ela.keras")


app_config = FastAPIConfig()
model_config = CNNModelConfig()
