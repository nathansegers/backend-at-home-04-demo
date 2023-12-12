from pydantic import BaseModel
from typing import Dict, List, Optional

class Book(BaseModel):
    id: Optional[int]
    title: str
    author: str
    year: int
    publisher: str
    description: str

    class Config:
        orm_mode = True

class UpdateBook(BaseModel):
    id: int
    author: Optional[str]
    year: Optional[int]
    description: Optional[str]

class DeleteBook(BaseModel):
    id: int

class DeleteBookResponse(BaseModel):
    message: str