"""Note application service (use cases)."""

from src.modules.note.application.schemas import NoteCreate, NoteUpdate
from src.modules.note.domain.model import Note
from src.modules.note.domain.repository import NoteRepository


class NoteError(Exception):
    """Base exception for the note domain. Raise subclasses from the service."""


class NoteNotFound(NoteError):
    """Raised when the requested note does not exist."""


class NoteService:
    """Application service for note use cases. Free of HTTP concerns."""

    def __init__(self, repository: NoteRepository) -> None:
        self._entities = repository

    @classmethod
    def from_repository(cls, repository: NoteRepository) -> "NoteService":
        return cls(repository)

    async def create(self, data: NoteCreate) -> Note:
        return await self._entities.add(Note(**data.model_dump()))

    async def list(self) -> list[Note]:
        return await self._entities.list()

    async def get(self, item_id: int) -> Note:
        entity = await self._entities.get(item_id)
        if entity is None:
            raise NoteNotFound()
        return entity

    async def update(self, item_id: int, data: NoteUpdate) -> Note:
        entity = await self.get(item_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(entity, field, value)
        return await self._entities.add(entity)

    async def delete(self, item_id: int) -> None:
        entity = await self.get(item_id)
        await self._entities.delete(entity)
