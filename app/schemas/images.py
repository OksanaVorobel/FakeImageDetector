from typing import Optional

from pydantic import BaseModel


class BaseImage(BaseModel):
    id: int
    image_url: str
    percentage_of_falsity: Optional[float] = None
    user_id: int


class OriginalImage(BaseImage):
    pass


class ELAImage(BaseImage):
    original_image_id: int


class ImageDetail(BaseImage):
    ela_image_url: str


class PredictFakeImage(BaseModel):
    real: float
    fake: float
