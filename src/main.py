from fastapi import FastAPI

from src import lifespan
from src.core.config import settings

app = FastAPI(
    app_name=settings.app_name,
    version="0.1.0",
    description="FastApi 练习项目实战",
)