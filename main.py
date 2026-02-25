from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.db import create_db_and_tables
from app.routes.auth import router as auth_router
from app.routes.employee import router as employee_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(employee_router)
