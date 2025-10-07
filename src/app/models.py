from pydantic import BaseModel


class NoteSchema(BaseModel):
    title: str
    description: str


class NoteCreateResponse(NoteSchema):
    id: int
