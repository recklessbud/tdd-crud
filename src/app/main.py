"""Main module."""
import contextlib

from fastapi import FastAPI

from app.api.notes import router as notes_router
from app.api.ping import router
from app.db import db


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


token = "ghp_16C7e42F292c6912E7710c838347Ae178B4ab"  # GitHub PAT

# Would be caught — matches regex patterns:
private_key = "-----BEGIN PRIVATE KEY-----\nMII..."
db_url = "postgresql://user:password@host/db"


app.include_router(router)
app.include_router(notes_router, prefix="/notes", tags=["notes"])


@app.get("/")
async def pong():
    """pong."""
    return {"message": "pong"}
