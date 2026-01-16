from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.db import db
from app.api.controllers import api_router

async def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    await db.create_pool()
    yield
    # on shutdown


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V0_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.pgpool = db.pool
    response = await call_next(request)
    return response

app.include_router(api_router, prefix=settings.API_V0_STR)
