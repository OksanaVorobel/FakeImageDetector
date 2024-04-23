import asyncio
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from app.db.connections import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    images = relationship("Image", back_populates="user")


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(256))
    status = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user = relationship('User', back_populates='images')
    ela_image = relationship('ELAImage', uselist=False, back_populates='original_image')


class ELAImage(Base):
    __tablename__ = 'ela_images'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(256))
    status = Column(Boolean)
    original_image_id = Column(Integer, ForeignKey('images.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    original_image = relationship('Image', back_populates='ela_image')


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# asyncio.run(init_models())
