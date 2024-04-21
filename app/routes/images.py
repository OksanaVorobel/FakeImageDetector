import random
import shutil
import string

from fastapi import APIRouter, Depends, UploadFile, File
from starlette import status

from app.db.models import User
from app.schemas.images import AddImage, ImageDetail
from app.services.auth import auth_service
from app.repositories.dependencies import users_service
from app.services.images import ImageService, ELAImageService

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/add", response_model=ImageDetail, status_code=status.HTTP_201_CREATED)
async def add_images(
        origin_image: AddImage,
        ela_image: AddImage,
        service: ImageService = Depends(users_service),
        ela_service: ELAImageService = Depends(users_service),
        current_user: User = Depends(auth_service.get_current_user)
):
    image = await service.add_image(origin_image)
    ela_image = await ela_service.add_image(ela_image, image.id)
    return {**image._dict_(), "ela_image_url": ela_image.image_url}


@router.post('/upload')
def load_image(
        image: UploadFile = File(...),
        current_user: User = Depends(auth_service.get_current_user),
        ela_service: ELAImageService = Depends(users_service),
):
    letters = string.ascii_letters
    rand_str = "".join(random.choice(letters) for i in range(8))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit(".", 1))
    path = f"images_store/origin/{filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    ela_image = ela_service.convert_to_ela(filename)
    ela_path = f"images_store/ela/{filename}"
    with open(ela_path, "wb") as buffer:
        shutil.copyfileobj(ela_image, buffer)

    return {"origin": filename, "ela": ela_path}


@router.post("/{image_id}")
async def delete_images(
        image_id: int,
        service: ImageService = Depends(users_service),
        current_user: User = Depends(auth_service.get_current_user)
):
    await service.delete_image(image_id, current_user.id)

