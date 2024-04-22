from typing import Type, List

import numpy as np
from PIL import Image
from fastapi import HTTPException
from starlette import status

from app.core.config import model_config
from app.repositories.images import ImageRepository, ELAImageRepository
from app.schemas.images import AddImage, ImageDetail
from app.utils.utils import convert_to_ela_image, load_fake_detection_model


class ImageService:
    def __init__(self, image_repo: Type[ImageRepository]):
        self.image_repo: ImageRepository = image_repo()

    async def add_image(self, image: AddImage, user_id: int):
        return await self.image_repo.add_one({**image.model_dump(), "user_id": user_id})

    async def get_users_images(self, user_id: int, limit: int, offset: int):
        return await self.image_repo.filter_by(limit, offset, {"user_id": user_id})

    async def get_all_users_images(self, user_id: int, limit: int = 10, offset: int = 0):
        images = await self.image_repo.get_all_users_images(limit, offset, {"user_id": user_id})
        base_images: List[ImageDetail] = []
        for image in images:
            base_image = ImageDetail(
                **image.__dict__,
                ela_image_url=image.ela_image.image_url
            )
            base_images.append(base_image)

        return base_images

    async def get_images(self, user_id: int, image_id: int):
        image = await self.image_repo.get_images({"user_id": user_id, "id": image_id})
        base_image = ImageDetail(
                **image.__dict__,
                ela_image_url=image.ela_image.image_url
            )
        return base_image

    async def delete_image(self, image_id: int, current_user_id: int):
        image = await self.image_repo.find_by_filter({"id": image_id})
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if current_user_id != image.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        await self.image_repo.delete_by_id(image_id)


class ELAImageService:
    cnn_model = load_fake_detection_model()

    def __init__(self, image_repo: Type[ELAImageRepository]):
        self.ela_image_repo: ELAImageRepository = image_repo()

    async def add_image(self, image: AddImage, origin_image_id):
        return await self.ela_image_repo.add_one(
            {**image.model_dump(), "original_image_id": origin_image_id}
        )

    async def delete_image(self, image_id: int):
        image = await self.ela_image_repo.find_by_filter({"id": image_id})
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await self.ela_image_repo.delete_by_id(image_id)

    @staticmethod
    def preprocess_image(image_path):
        img = Image.open(image_path)
        img = img.resize(
            (model_config.img_height, model_config.img_width), resample=Image.LANCZOS
        )
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    @staticmethod
    def convert_to_ela(image_path):
        return convert_to_ela_image(image_path)

    def predict_image(self, image_path):
        img_array = self.preprocess_image(image_path)
        prediction = self.cnn_model.predict(img_array)
        return {"real": float(prediction[0][0]), "fake": float(prediction[0][1])}


image_server = ImageService(ImageRepository)
ela_image_service = ELAImageService(ELAImageRepository)
