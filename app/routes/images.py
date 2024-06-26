import os
import random
import string
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from starlette import status

from app.db.models import User
from app.schemas.images import ImageDetail, PredictFakeImage
from app.services.auth import auth_service
from app.repositories.dependencies import ela_images_service, images_service
from app.services.images import ImageService, ELAImageService

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/detect", status_code=status.HTTP_200_OK)
async def detect_fake(
        image_url: str,
        ela_service: ELAImageService = Depends(ela_images_service),
        current_user: User = Depends(auth_service.get_current_user)
) -> PredictFakeImage:
    prediction = ela_service.predict_image(image_url)
    return prediction


@router.post("/add", response_model=ImageDetail, status_code=status.HTTP_201_CREATED)
async def add_images(
        origin_image_url: str,
        ela_image_url: str,
        percentage_of_falsity: float,
        service: ImageService = Depends(images_service),
        ela_service: ELAImageService = Depends(ela_images_service),
        current_user: User = Depends(auth_service.get_current_user)
):
    image_id = await service.add_image(origin_image_url, percentage_of_falsity, current_user.id)
    await ela_service.add_image(ela_image_url, image_id)
    return {
        "id": image_id,
        "image_url": origin_image_url,
        "ela_image_url": ela_image_url,
        "user_id": current_user.id,
        "percentage_of_falsity": percentage_of_falsity,
    }


@router.post('/upload')
def load_image(
        image: UploadFile = File(...),
        current_user: User = Depends(auth_service.get_current_user),
        ela_service: ELAImageService = Depends(ela_images_service),
) -> dict:
    letters = string.ascii_letters
    rand_str = "".join(random.choice(letters) for i in range(8))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit(".", 1))
    path = f"../images_store/origin/{filename}"
    with open(path, "wb") as f:
        f.write(image.file.read())

    ela_image = ela_service.convert_to_ela(path)
    ela_path = f"../images_store/ela/{filename}"
    ela_image.save(ela_path)

    return {"origin": path, "ela": ela_path}


@router.get('/by-path')
def get_image_by_path(image_path: str):
    if not os.path.exists(image_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return FileResponse(image_path)


@router.get("/{image_id}", status_code=status.HTTP_200_OK)
async def get_image_by_id(
        image_id: int,
        service: ImageService = Depends(images_service),
        current_user: User = Depends(auth_service.get_current_user)
) -> ImageDetail:
    return await service.get_images(current_user.id, image_id)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_images(
        service: ImageService = Depends(images_service),
        current_user: User = Depends(auth_service.get_current_user)
) -> List[ImageDetail]:
    return await service.get_all_users_images(current_user.id)


@router.delete("/{image_id}")
async def delete_image(
        image_id: int,
        service: ImageService = Depends(images_service),
        current_user: User = Depends(auth_service.get_current_user)
):
    await service.delete_image(image_id, current_user.id)
