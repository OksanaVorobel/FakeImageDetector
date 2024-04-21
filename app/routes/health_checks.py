import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connections import get_db

router = APIRouter(tags=["healthcheck"])


@router.get("/")
async def health_check():
    return {"status_code": 200, "detail": "ok", "result": "working"}


@router.get("/db_connection")
async def check_db_connection(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        if result is None:
            logging.error("PostgreSQL is not configured correctly")
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"status_code": 200, "detail": "ok", "result": "working"}
    except Exception as e:
        logging.error("Some problems with connection to PostgreSQL")
        raise HTTPException(status_code=500, detail="Error connecting to the database")
