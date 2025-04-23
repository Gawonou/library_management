from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    subtitle = Column(String(255), nullable=True)
    author = Column(String(255), nullable=False)
    publisher = Column(String(255), nullable=True)
    published_date = Column(DateTime, nullable=True)
    isbn_10 = Column(String(10), unique=True, nullable=True, index=True)
    isbn_13 = Column(String(13), unique=True, nullable=True, index=True)
    pages = Column(Integer, nullable=True)
    language = Column(String(50), nullable=True)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    description = Column(String, nullable=True)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationship: one book can have multiple loans
    loans = relationship("Loan", back_populates="book")