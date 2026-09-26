"""SQLAlchemy adapter for the Note repository port."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.note.domain.model import Note


class SqlNoteRepository:
    """Implements :class:`src.modules.note.domain.repository.NoteRepository`."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, entity: Note) -> Note:
        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def get(self, entity_id: int) -> Note | None:
        return await self._session.get(Note, entity_id)

    async def list(self) -> list[Note]:
        result = await self._session.scalars(select(Note))
        return list(result)

    async def delete(self, entity: Note) -> None:
        await self._session.delete(entity)
        await self._session.commit()
