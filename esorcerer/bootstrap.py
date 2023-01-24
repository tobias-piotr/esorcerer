from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from esorcerer.settings import settings


def add_cors_middleware(app: FastAPI) -> None:
    """Add CORS middleware."""
    origins = ["*"] if settings.DEBUG else settings.CORS_ALLOW_ORIGINS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# TODO: Add more middleware
def bootstrap(app: FastAPI) -> FastAPI:
    """Run everything needed before the app starts."""
    add_cors_middleware(app)
    return app
