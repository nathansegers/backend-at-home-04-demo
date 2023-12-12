from typing import List, Optional
import strawberry
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

# ENUMS
@strawberry.enum
class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

# BOOKS

class BaseBook(BaseModel):
    id: Optional[int]

class Book(BaseBook):
    title: str
    author_id: int
    year: int
    publisher: str
    description: str

    class Config:
        orm_mode = True

class DeleteBook(BaseBook):
    id: int # Required here!

class UpdateBook(BaseBook):
    id: int # Required here!
    title: Optional[str]
    year: Optional[str]
    publisher: Optional[str]
    description: Optional[str]

# AUTHORS

class BaseAuthor(BaseModel):
    id: Optional[int]

class Author(BaseAuthor):
    name: str
    birthdate: datetime
    gender: Gender

    class Config:
        orm_mode = True
        use_enum_values = True

class DeleteAuthor(BaseAuthor):
    id: int # Required here!

# Viewmodels

class BookViewModel(Book):
    author: Author

class AuthorViewModel(Author):
    books: List[Book]

# Generic models

class DeleteResponse(BaseModel):
    message: str
