import sentry_sdk
from fastapi import FastAPI

from app.dependencies.settings import get_settings
from app.startup.startup import create_app

settings = get_settings()
sentry_sdk.init(
    dsn=settings.monitoring.sentry_dsn,
    traces_sample_rate=settings.monitoring.traces_sample_rate,
    profiles_sample_rate=settings.monitoring.profiles_sample_rate,
)

app: FastAPI = create_app()


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.get("/healthcheck")
async def healthcheck() -> dict:
    return {"message": "Hello World"}
