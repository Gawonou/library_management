from pydantic import BaseModel, Field
from typing import Optional, List
import datetime
from .loan import Loan as LoanSchema

class BookBase(BaseModel):
    title: str = Field(..., max_length=255)
    subtitle: Optional[str] = None
    author: str = Field(..., max_length=255)
    publisher: Optional[str] = None
    published_date: Optional[datetime.datetime] = None
    isbn_10: Optional[str] = Field(None, max_length=10)
    isbn_13: Optional[str] = Field(None, max_length=13)
    pages: Optional[int] = None
    language: Optional[str] = None
    total_copies: int = 1
    available_copies: int = 1
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str]
    subtitle: Optional[str]
    author: Optional[str]
    publisher: Optional[str]
    published_date: Optional[datetime.datetime]
    isbn_10: Optional[str]
    isbn_13: Optional[str]
    pages: Optional[int]
    language: Optional[str]
    total_copies: Optional[int]
    available_copies: Optional[int]
    description: Optional[str]
    available: Optional[bool]

class BookInDBBase(BookBase):
    id: int
    available: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True 

class Book(BookInDBBase):
    loans: List[LoanSchema] = []
