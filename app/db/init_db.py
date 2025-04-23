"""
Initialize the database: create tables and optionally seed initial data.
"""
from app.db.base import Base
from app.db.session import engine


def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # TODO: add seed data here if needed
    # Example:
    # from app.models.user import User
    # from app.services.user_service import create_user
    # from app.schemas.user import UserCreate


if __name__ == '__main__':
    init_db()
    print("Database initialized!")
