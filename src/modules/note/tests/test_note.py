from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from src.modules import modules
from src.modules.note.api.router import router


def test_module_registered() -> None:
    assert modules["note"] == "src.modules.note"


def test_router_prefix() -> None:
    assert router.prefix == "/notes"


async def test_db_available(db_engine: AsyncEngine) -> None:
    async with db_engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar_one() == 1


async def test_notes_crud(client: AsyncClient) -> None:
    created = await client.post("/notes", json={"title": "first", "content": "hello"})
    assert created.status_code == 201, created.text
    note = created.json()
    assert note["title"] == "first"
    assert note["done"] is False

    listed = await client.get("/notes")
    assert listed.status_code == 200
    assert [n["id"] for n in listed.json()] == [note["id"]]

    fetched = await client.get(f"/notes/{note['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["content"] == "hello"

    patched = await client.patch(f"/notes/{note['id']}", json={"done": True})
    assert patched.status_code == 200
    assert patched.json()["done"] is True

    deleted = await client.delete(f"/notes/{note['id']}")
    assert deleted.status_code == 204
    assert (await client.get(f"/notes/{note['id']}")).status_code == 404


async def test_create_note_validates_title(client: AsyncClient) -> None:
    response = await client.post("/notes", json={"title": ""})
    assert response.status_code == 422
