from app.db import db, notes
from app.models import NoteSchema


async def crud_notes_create(note: NoteSchema):
    query = notes.insert().values(title=note.title, description=note.description)
    note_id = await db.execute(query)
    return note_id


async def getSingle(id: int):
    query = notes.select().where(id == notes.c.id)
    fetch = await db.fetch_one(query=query)
    return fetch



async def fetch_all():
    fetch_notes = notes.select()
    return await db.fetch_all(query=fetch_notes)


async def put_data(id: int, payload):
    query = (
        notes.update()
        .where(id == notes.c.id)
        .values(title=payload.title, description=payload.description)
        .returning(notes.c.id)
    )
    return await db.execute(query=query)


async def delete_data(id):
    query = notes.delete().where(id == notes.c.id)
    return await db.execute(query=query)
