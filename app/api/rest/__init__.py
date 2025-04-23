from fastapi import APIRouter
from .book import router as book_router
# from .user import router as user_router   # if you have one
# from .loan import router as loan_router   # if you have one

api_router = APIRouter()
api_router.include_router(book_router, prefix="/books", tags=["books"])
# api_router.include_router(user_router, prefix="/users", tags=["users"])
# api_router.include_router(loan_router, prefix="/loans", tags=["loans"])