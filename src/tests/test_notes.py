import json

import pytest

from app.api import notes


def test_create_note(test_client, monkeypatch):
    test_request_payload = {"title": "thhing", "description": "ption"}
    test_response_payload = {"id": 4, "title": "thhing", "description": "ption"}

    async def mock_crud_create_notes(payload):
        return 4

    monkeypatch.setattr(notes, "crud_notes_create", mock_crud_create_notes)

    response = test_client.post(
        "/notes/",
        json=test_request_payload,
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_note_invalid_json(test_client):
    response = test_client.post("/notes/", content=json.dumps({"title": "something"}))
    assert response.status_code == 422


def test_get_notes(test_client, monkeypatch):
    test_data = {"id": 3, "title": "foo", "description": "bar"}

    async def mock_get_data(id):
        return test_data

    monkeypatch.setattr(notes, "getSingle", mock_get_data)
    response = test_client.get("/notes/3")
    assert response.status_code == 200
    assert response.json() == test_data


def test_invalid_id(test_client, monkeypatch):
    async def mock_get_data(id):
        return None

    monkeypatch.setattr(notes, "getSingle", mock_get_data)
    response = test_client.get("/notes/999")
    assert response.status_code == 404


def test_get_all(test_client, monkeypatch):
    test_data = [
        {"id": 3, "title": "foo", "description": "bar"},
        {"id": 4, "title": "fizz", "description": "buzz"},
    ]

    async def mock_fetch_all():
        return test_data

    monkeypatch.setattr(notes, "fetch_all", mock_fetch_all)
    response = test_client.get("/notes/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_get_all_empty(test_client, monkeypatch):
    async def mock_fetch_all():
        return []

    monkeypatch.setattr(notes, "fetch_all", mock_fetch_all)
    response = test_client.get("/notes/")
    assert response.status_code == 404


def test_update_note(test_client, monkeypatch):
    test_request_payload = {"title": "thhing", "description": "ption"}
    test_response_payload = {"id": 4, "title": "thhing", "description": "ption"}

    async def mock_update_service(id):
        return True

    async def mock_put_data(id, payload):
        return 4

    monkeypatch.setattr(notes, "getSingle", mock_update_service)

    monkeypatch.setattr(notes, "put_data", mock_put_data)

    request = test_client.put("/notes/4", json=test_request_payload)
    assert request.status_code == 200
    assert request.json() == test_response_payload


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [4, {}, 422],
        [4, {"description": "bar"}, 422],
        [498, {"title": "foo", "description": "bar"}, 404],
    ],
)
def test_update_note_invalid(test_client, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(notes, "getSingle", mock_get)
    request = test_client.put(f"/notes/{id}", json=payload)
    assert request.status_code == status_code


def test_delete_note(test_client, monkeypatch):
    test_data = {"id": 4, "title": "foo", "description": "bar"}

    async def mock_get(id):
        return test_data

    async def mock_delete(id):
        return id

    monkeypatch.setattr(notes, "getSingle", mock_get)
    monkeypatch.setattr(notes, "delete_data", mock_delete)

    request = test_client.delete("/notes/4")
    assert request.status_code == 204


def test_remove_note_incorrect_id(test_client, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(notes, "getSingle", mock_get)

    response = test_client.delete("/notes/999/")
    assert response.status_code == 404
