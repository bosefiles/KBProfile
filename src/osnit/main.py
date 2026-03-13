from contextlib import asynccontextmanager

from fastapi import FastAPI

from osnit.api.routes import india_repository, router
from osnit.services.india_footprint import IndiaFootprintScheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = IndiaFootprintScheduler(repository=india_repository, interval_seconds=1800)
    await scheduler.start()
    app.state.india_scheduler = scheduler
    yield
    await scheduler.stop()


def create_app() -> FastAPI:
    app = FastAPI(
        title="OSNIT",
        description="Python-based OSINT platform MVP inspired by analyst workflows.",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(router, prefix="/api/v1")
    return app


app = create_app()
