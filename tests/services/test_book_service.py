import pytest
from app.services.book_service import create_book, get_books, get_book, update_book, delete_book
from app.schemas.book import BookCreate, BookUpdate

@ pytest.mark.usefixtures("db_session")
def test_book_crud(db_session):
    # Create a book
    book_in = BookCreate(
        title="Test Book", author="Author A", description="Desc.", pages=100, isbn_10="1234567890"
    )
    book = create_book(db_session, book_in)
    assert book.id is not None
    assert book.title == "Test Book"

    # Read books
    books = get_books(db_session)
    assert len(books) == 1

    # Get single book
    fetched = get_book(db_session, book.id)
    assert fetched.id == book.id

    # Update book
    update_data = BookUpdate(title="Updated Title", available=False)
    updated = update_book(db_session, book.id, update_data)
    assert updated.title == "Updated Title"
    assert not updated.available

    # Delete book
    deleted = delete_book(db_session, book.id)
    assert deleted.id == book.id
    assert get_book(db_session, book.id) is None