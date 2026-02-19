from fastapi import FastAPI

from osnit.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="OSNIT",
        description="Python-based OSINT platform MVP inspired by analyst workflows.",
        version="0.1.0",
    )
    app.include_router(router, prefix="/api/v1")
    return app


app = create_app()
