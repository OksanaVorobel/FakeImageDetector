from typing import Type

from fastapi import HTTPException
from starlette import status

from app.cnn_model.data_preprocessing import convert_to_ela_image
from app.repositories.images import ImageRepository, ELAImageRepository
from app.schemas.images import AddImage


class ImageService:
    def __init__(self, image_repo: Type[ImageRepository]):
        self.image_repo: ImageRepository = image_repo()

    async def add_image(self, image: AddImage):
        return await self.image_repo.add_one(image.model_dump())

    async def get_users_images(self, user_id: int, limit: int, offset: int):
        return await self.image_repo.filter_by(limit, offset, {"user_id": user_id})

    async def get_all_users_images(self, user_id: int, limit: int, offset: int):
        images = await self.image_repo.get_all_users_images(limit, offset,{"user_id": user_id})
        return images

    async def delete_image(self, image_id: int, current_user_id: int):
        image = await self.image_repo.find_by_filter({"id": image_id})
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if current_user_id != image.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        await self.image_repo.delete_by_id(image_id)


class ELAImageService:
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
    def convert_to_ela(image_path):
        return convert_to_ela_image(image_path)


image_server = ImageService(ImageRepository)
ela_image_service = ELAImageService(ELAImageRepository)
