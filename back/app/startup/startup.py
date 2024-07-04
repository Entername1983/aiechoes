from contextlib import asynccontextmanager

from app.config.posthog import setup_post_hog
from app.routes.replies import replies_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute


def setup_routes(app):
    app.include_router(replies_router)


def custom_generate_unique_id(route: APIRoute):
    """USE for SDK generation"""
    return f"{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting lifespan")
    app.state.posthog = setup_post_hog()
    yield


def create_app():
    print("Creating app")
    app = FastAPI(
        generate_unique_id_function=custom_generate_unique_id, lifespan=lifespan
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
