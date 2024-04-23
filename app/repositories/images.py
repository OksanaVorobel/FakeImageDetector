from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.connections import async_session
from app.db.models import Image, ELAImage
from app.utils.repository import SQLAlchemyRepository


class ImageRepository(SQLAlchemyRepository):
    model = Image

    async def get_all_users_images(self, limit: int, offset: int, filter_by: dict) -> list:
        async with async_session() as session:
            statement = (
                select(self.model)
                .filter_by(**filter_by)
                .options(selectinload(Image.ela_image))
                .limit(limit)
                .offset(offset)
            )
            res = await session.execute(statement)
            return res.scalars().all()

    async def get_images(self, filter_by: dict):
        async with async_session() as session:
            statement = (
                select(self.model)
                .filter_by(**filter_by)
                .options(selectinload(Image.ela_image))
            )
            res = await session.execute(statement)
            return res.scalar_one()


class ELAImageRepository(SQLAlchemyRepository):
    model = ELAImage
