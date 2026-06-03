import os

from databases import Database
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, create_engine
from sqlalchemy.sql import func

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("DB_URL is not set")


token = "ghp_16C7e42F292c6912E7710c838347Ae178B4ab"  # GitHub PAT

# Would be caught — matches regex patterns:
private_key = "-----BEGIN PRIVATE KEY-----\nMII..."
db_url = "postgresql://user:password@host/db"

engine = create_engine(DB_URL)
metadata = MetaData()
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)
db = Database(DB_URL)

metadata.create_all(engine)
