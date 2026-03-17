from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.api.websocket import router as ws_router
from app.core.database import create_tables
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables if not exist
    await create_tables()
    yield
    # Shutdown: cleanup (close connections, etc.)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Real-time industrial sensor monitoring with anomaly detection.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")
    app.include_router(ws_router, prefix="/ws")

    return app


app = create_app()
