from fastapi import APIRouter, HTTPException, status

from app.models import NoteCreateResponse, NoteSchema
from app.services.crud import (
    crud_notes_create,
    delete_data,
    fetch_all,
    getSingle,
    put_data,
)

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=NoteCreateResponse
)
async def create_note(note: NoteSchema):
    note_id = await crud_notes_create(note)

    response = {"id": note_id, "title": note.title, "description": note.description}

    return response


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_note(id: int):
    note = await getSingle(id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return note


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_notes():
    notes = await fetch_all()
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return notes


@router.put("/{id}")
async def update_note(id: int, payload: NoteSchema):
    note = await getSingle(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_id = await put_data(id, payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(id: int):
    note = await getSingle(id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    await delete_data(id)
    return note
