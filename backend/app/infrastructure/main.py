from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.adapters.inbound.api_router import router as api_router
from app.adapters.inbound.health_router import router as health_router
from app.infrastructure.config import Settings


_FRONTEND_DIST_PATH = Path(__file__).resolve().parents[2] / "frontend_dist"


def get_frontend_dist_path() -> Path:
    return _FRONTEND_DIST_PATH


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = Settings()
    Path(settings.audio_storage_path).mkdir(parents=True, exist_ok=True)
    yield


def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(title="WordSound API", version="0.1.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)
    app.include_router(health_router)

    frontend_dist_path = get_frontend_dist_path()
    if frontend_dist_path.exists():

        @app.get("/", include_in_schema=False)
        async def serve_frontend_index():
            return FileResponse(frontend_dist_path / "index.html")

        @app.get("/{full_path:path}", include_in_schema=False)
        async def serve_frontend_asset(full_path: str):
            requested_path = (frontend_dist_path / full_path).resolve()
            try:
                requested_path.relative_to(frontend_dist_path.resolve())
            except ValueError:
                return FileResponse(frontend_dist_path / "index.html")

            if requested_path.is_file():
                return FileResponse(requested_path)
            return FileResponse(frontend_dist_path / "index.html")

    return app


app = create_app()
