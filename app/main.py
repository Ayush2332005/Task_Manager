from fastapi import FastAPI

from app.database import (
    engine,
    Base
)

from app.models import *

from app.routers import (
    auth,
    task
)


Base.metadata.create_all(
    bind=engine
)


app=FastAPI()


app.include_router(
    auth.router
)


app.include_router(
    task.router
)