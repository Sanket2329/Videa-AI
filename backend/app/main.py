"""FastAPI application factory.

Creates and configures the FastAPI app with:
  - CORS middleware
  - Exception handlers for custom AppException hierarchy
  - Versioned API routes (/api/v1/...)
  - Structured logging
  - OpenAPI documentation
"""

import os
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import health, prompts, videos
from app.core.config import get_settings
from app.core.exceptions import AppException
from app.core.logging import get_logger, setup_logging

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown events."""
    settings = get_settings()
    setup_logging(debug=settings.DEBUG)
    logger.info(
        "app_starting",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        provider=settings.VIDEO_PROVIDER,
        model=settings.VIDEO_MODEL,
        debug=settings.DEBUG,
    )
    yield
    logger.info("app_shutting_down")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "AI-powered video generation platform. Enter a natural-language "
            "description and generate short AI videos with optional LLM "
            "prompt enhancement."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # --- CORS ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Static Files ---
    os.makedirs("static/videos", exist_ok=True)
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # --- Exception Handlers ---
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        """Handle all custom application exceptions with consistent format."""
        logger.warning(
            "app_exception",
            code=exc.code,
            message=exc.message,
            status_code=exc.status_code,
            path=str(request.url),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "data": None,
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                },
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Catch-all handler — logs internals but returns a safe message."""
        logger.error(
            "unhandled_exception",
            error=str(exc),
            error_type=type(exc).__name__,
            path=str(request.url),
        )
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "data": None,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred. Please try again.",
                },
            },
        )

    # --- Routes ---
    app.include_router(health.router, prefix="/api/v1")
    app.include_router(prompts.router, prefix="/api/v1")
    app.include_router(videos.router, prefix="/api/v1")

    return app


# Application instance for uvicorn
app = create_app()
