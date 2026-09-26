from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    """Shared note fields."""

    title: str = Field(min_length=1, max_length=200)
    content: str = ""
    done: bool = False


class NoteCreate(NoteBase):
    """Payload for creating a note."""


class NoteUpdate(BaseModel):
    """Payload for updating a note — every field optional."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = None
    done: bool | None = None


class NoteRead(NoteBase):
    """Response schema. ``from_attributes`` lets FastAPI serialize ORM objects."""

    model_config = ConfigDict(from_attributes=True)

    id: int
