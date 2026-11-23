import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import __version__
from app.core.config import get_settings
from app.core.logger import setup_logging, get_logger
from app.core.exceptions import register_exception_handlers

settings = get_settings()
logger = get_logger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    Handles startup bootstrapping (directory initialization, logging config)
    and graceful shutdown routines.
    """
    # 1. Initialize logging
    setup_logging(log_level=settings.log_level, is_production=settings.is_production)
    logger.info(
        f"Booting {settings.app_name} v{__version__} in [{settings.app_env.upper()}] mode",
        extra={
            "debug": settings.debug,
            "gemini_model": settings.gemini_model,
            "has_langfuse": settings.has_langfuse,
        }
    )

    # 2. Ensure data directories exist
    os.makedirs(settings.upload_directory, exist_ok=True)
    os.makedirs(settings.chroma_persist_directory, exist_ok=True)
    logger.info(f"Verified storage directories at '{settings.upload_directory}' and '{settings.chroma_persist_directory}'")

    yield

    # 3. Graceful shutdown
    logger.info(f"Shutting down {settings.app_name} gracefully.")


def create_app() -> FastAPI:
    """
    FastAPI Application Factory.
    Configures middleware, exception handlers, routers, and lifecycle hooks.
    """
    app = FastAPI(
        title="Enterprise Candidate Intelligence & Screening Agent",
        description="Autonomous, audit-ready AI system for candidate resume screening using Hybrid RAG and LangGraph HITL.",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Standardized Exception Handlers
    register_exception_handlers(app)

    # Root / Info Endpoint
    @app.get("/", tags=["System"])
    async def root():
        return {
            "name": settings.app_name,
            "version": __version__,
            "status": "online",
            "environment": settings.app_env,
            "docs": "/docs",
        }

    # Health Check Endpoint
    @app.get("/health", tags=["System"], status_code=status.HTTP_200_OK)
    async def health_check():
        return {
            "status": "healthy",
            "version": __version__,
            "gemini_configured": bool(settings.gemini_api_key),
            "langfuse_configured": settings.has_langfuse,
        }

    return app


app = create_app()

