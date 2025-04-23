import graphene
from graphene import ObjectType, Field, List, Int, String, Boolean, Mutation
from app.services.book_service import (
    get_book, get_books, create_book, update_book, delete_book
)
from app.schemas.book import BookCreate as BookCreateSchema, BookUpdate as BookUpdateSchema
from app.db.session import SessionLocal
from app.models.book import Book as BookModel

class BookType(ObjectType):
    id = Int()
    title = String()
    subtitle = String()
    author = String()
    publisher = String()
    published_date = String()  # ISO format
    isbn_10 = String()
    isbn_13 = String()
    pages = Int()
    language = String()
    total_copies = Int()
    available_copies = Int()
    description = String()
    available = Boolean()
    created_at = String()
    updated_at = String()

class Query(ObjectType):
    books = List(BookType, skip=Int(), limit=Int())
    book = Field(BookType, id=Int(required=True))

    def resolve_books(self, info, skip=0, limit=100):
        db = SessionLocal()
        books = get_books(db, skip, limit)
        db.close()
        return books

    def resolve_book(self, info, id):
        db = SessionLocal()
        book = get_book(db, id)
        db.close()
        return book

class CreateBook(Mutation):
    class Arguments:
        title = String(required=True)
        subtitle = String()
        author = String(required=True)
        publisher = String()
        published_date = String()
        isbn_10 = String()
        isbn_13 = String()
        pages = Int()
        language = String()
        total_copies = Int()
        available_copies = Int()
        description = String()

    book = Field(lambda: BookType)

    def mutate(self, info, **kwargs):
        db = SessionLocal()
        book_in = BookCreateSchema(**kwargs)
        new_book = create_book(db, book_in)
        db.close()
        return CreateBook(book=new_book)

class UpdateBook(Mutation):
    class Arguments:
        id = Int(required=True)
        title = String()
        subtitle = String()
        author = String()
        publisher = String()
        published_date = String()
        isbn_10 = String()
        isbn_13 = String()
        pages = Int()
        language = String()
        total_copies = Int()
        available_copies = Int()
        description = String()
        available = Boolean()

    book = Field(lambda: BookType)

    def mutate(self, info, id, **kwargs):
        db = SessionLocal()
        book_in = BookUpdateSchema(**kwargs)
        updated_book = update_book(db, id, book_in)
        db.close()
        return UpdateBook(book=updated_book)

class DeleteBook(Mutation):
    class Arguments:
        id = Int(required=True)

    ok = Boolean()

    def mutate(self, info, id):
        db = SessionLocal()
        deleted = delete_book(db, id)
        db.close()
        return DeleteBook(ok=bool(deleted))

class Mutation(ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)