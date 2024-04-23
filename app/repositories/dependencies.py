from app.repositories.images import ImageRepository, ELAImageRepository
from app.repositories.users import UsersRepository
from app.services.images import ImageService, ELAImageService
from app.services.users import UsersService


def users_service():
    return UsersService(UsersRepository)

def images_service():
    return ImageService(ImageRepository)

def ela_images_service():
    return ELAImageService(ELAImageRepository)
