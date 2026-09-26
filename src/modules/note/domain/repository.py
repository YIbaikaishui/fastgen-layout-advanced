"""Note repository port interface."""

from typing import Protocol

from src.modules.note.domain.model import Note


class NoteRepository(Protocol):
    """Persistence contract for ``Note`` entities."""

    async def add(self, entity: Note) -> Note: ...

    async def get(self, entity_id: int) -> Note | None: ...

    async def list(self) -> list[Note]: ...

    async def delete(self, entity: Note) -> None: ...
