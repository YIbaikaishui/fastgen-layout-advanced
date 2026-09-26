"""Note HTTP router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.modules.note.application.note_service import (
    NoteNotFound,
    NoteService,
)
from src.modules.note.application.schemas import (
    NoteCreate,
    NoteRead,
    NoteUpdate,
)
from src.modules.note.domain.model import Note
from src.modules.note.infrastructure.note_repository import SqlNoteRepository

SessionDep = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix="/notes", tags=["notes"])


def _service(session: AsyncSession) -> NoteService:
    return NoteService.from_repository(SqlNoteRepository(session))


@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(data: NoteCreate, session: SessionDep) -> Note:
    return await _service(session).create(data)


@router.get("", response_model=list[NoteRead])
async def list_notes(session: SessionDep) -> list[Note]:
    return await _service(session).list()


@router.get("/{note_id}", response_model=NoteRead)
async def get_note(note_id: int, session: SessionDep) -> Note:
    try:
        return await _service(session).get(note_id)
    except NoteNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


@router.patch("/{note_id}", response_model=NoteRead)
async def update_note(
    note_id: int, data: NoteUpdate, session: SessionDep
) -> Note:
    try:
        return await _service(session).update(note_id, data)
    except NoteNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, session: SessionDep) -> None:
    try:
        await _service(session).delete(note_id)
    except NoteNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
