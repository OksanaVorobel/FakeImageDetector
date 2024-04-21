import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes import health_checks, users

from app.core.config import app_config

app = FastAPI(title="Fake Image Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_checks.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=app_config.host, port=app_config.port, reload=True)
