import sentry_sdk
from fastapi import FastAPI

from app.startup.startup import create_app

sentry_sdk.init(
    dsn="https://78859ae67c9ee114c055c4349364e28c@o4506774392078336.ingest.us.sentry.io/4507526319505408",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/healthcheck")
async def healthcheck():
    return {"message": "Hello World"}
