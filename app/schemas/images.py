from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseImage(BaseModel):
    id: int
    image_url: str
    status: Optional[str] = None
    user_id: int


class AddImage(BaseModel):
    image_url: str
    status: Optional[str] = None


class OriginalImage(BaseImage):
    pass


class ELAImage(BaseImage):
    original_image_id: int


class ImageDetail(BaseImage):
    ela_image_url: str
