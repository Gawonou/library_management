from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.book import Book, BookCreate, BookUpdate
from app.services.book_service import (
    get_book, get_books, create_book, update_book, delete_book
)
from app.db.session import get_db

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_books(db, skip, limit)

@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.post("/", response_model=Book, status_code=201)
def create_new_book(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book)

@router.put("/{book_id}", response_model=Book)
def update_existing_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = update_book(db, book_id, book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.delete("/{book_id}", response_model=Book)
def delete_existing_book(book_id: int, db: Session = Depends(get_db)):
    db_book = delete_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

