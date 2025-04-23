import pytest
from fastapi import status


def test_create_read_update_delete_book(client):
    # Create via API
    response = client.post(
        "/api/books/", json={
            "title": "API Book", "author": "Api Author", "description": "API Desc.", "pages": 50
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    book_id = data["id"] if isinstance(data, list) else data.get("id")
    assert data["title"] == "API Book"

    # Read list
    response = client.get("/api/books/?skip=0&limit=10")
    assert response.status_code == status.HTTP_200_OK
    assert any(b["title"] == "API Book" for b in response.json())

    # Read single
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == book_id

    # Update
    response = client.put(
        f"/api/books/{book_id}", json={"title": "API Updated"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "API Updated"

    # Delete
    response = client.delete(f"/api/books/{book_id}")
    assert response.status_code == status.HTTP_200_OK

    # Confirm deletion
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
