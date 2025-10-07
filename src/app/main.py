"""Main module."""
import contextlib
from fastapi import FastAPI
from app.api.ping import router
from app.db import db

from app.api.notes import router as notes_router

@contextlib.asynccontextmanager
async def lifespan(src: FastAPI):
    """function for starting and shutting down the database."""
    try:
        await db.connect()
        print("db-connected")
        yield
    finally:
        await db.disconnect()
        print(f"db-disconnected, {src}")


app = FastAPI(lifespan=lifespan)


app.include_router(router)
app.include_router(notes_router, prefix="/notes", tags=["notes"])


@app.get("/")
async def pong():
    """pong."""
    return {"message": "pong"}
