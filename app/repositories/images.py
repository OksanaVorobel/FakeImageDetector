from sqlalchemy import select

from app.db.connections import async_session
from app.db.models import Image, ELAImage
from app.utils.repository import SQLAlchemyRepository


class ImageRepository(SQLAlchemyRepository):
    model = Image

    async def get_all_users_images(self, limit: int, offset: int, filter_by: dict) -> list:
        async with async_session() as session:
            statement = select(self.model, ELAImage.image_url).filter_by(**filter_by).limit(limit).offset(offset)
            res = await session.execute(statement)
            return res.scalars().all()


class ELAImageRepository(SQLAlchemyRepository):
    model = ELAImage