import json
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from app.config.posthog import setup_post_hog
from app.dependencies.settings import get_settings
from app.routes.replies import replies_router

logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all log messages
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Ensure logs go to the console
)
log = logging.getLogger("App")


def setup_routes(app: FastAPI) -> None:
    app.include_router(replies_router)


def custom_generate_unique_id(route: APIRoute) -> str:
    """USE for SDK generation"""
    return f"{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    log.info("starting lifespan")
    app.state.posthog = setup_post_hog()
    yield


settings = get_settings()


def create_app() -> FastAPI:
    log.info("Creating app")
    log.info(json.dumps(settings.model_dump(), indent=4))

    app = FastAPI(
        generate_unique_id_function=custom_generate_unique_id,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_routes(app)

    return app
