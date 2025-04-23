from pydantic import BaseModel
from typing import Optional
import datetime

class LoanBase(BaseModel):
    user_id: int
    book_id: int
    due_date: datetime.datetime

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    borrowed_at: datetime.datetime
    returned_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True 

