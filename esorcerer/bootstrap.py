from fastapi import FastAPI, Request, responses
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from esorcerer.domain import exceptions
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


def setup_orm(app: FastAPI) -> None:
    """Setup database ORM."""
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["esorcerer.plugins.database.models"]},
        # TODO: Replace with aerich
        generate_schemas=True,
        add_exception_handlers=True,
    )


def add_exception_handlers(app: FastAPI) -> None:
    """Add exception handlers."""

    def handle_domain_exc(
        request: Request,
        exc: exceptions.DomainError,
    ) -> responses.JSONResponse:
        return responses.JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    app.add_exception_handler(exceptions.DomainError, handle_domain_exc)


# TODO: Add more middleware
def bootstrap(app: FastAPI) -> FastAPI:
    """Run everything needed before the app starts."""
    add_cors_middleware(app)
    setup_orm(app)
    add_exception_handlers(app)
    return app
