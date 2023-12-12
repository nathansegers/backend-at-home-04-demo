from typing import Optional, List, Union
import strawberry

from .exceptions import BookNotFoundException
from shared import BaseError
from graphql_models import BookInput, BookNotFoundError, ListOfBooks, BookType, BookResponse
from models import BookViewModel, Book
from .repository import BookRepository

@strawberry.type
class Query:
    @strawberry.field
    def books(self) -> Union[ListOfBooks, BaseError]:
        try:
            books: List[BookType] = BookRepository.get_all()
            # books = [] # Uncomment this if you want to test having no books!
            if (len(books) > 0):
                return ListOfBooks(books=books)
            else:
                raise BookNotFoundException(f"No books found")
                
        except BookNotFoundException as e:
            return BaseError(error=str(e))

    @strawberry.field
    def book(self,
        title: Optional[str] = strawberry.UNSET,
        id: Optional[int] = strawberry.UNSET,
    ) -> BookResponse:
        try:
            if (title is not strawberry.UNSET):
                book: BookType = BookRepository.get_by(title=title)
                if (book is None):
                    raise BookNotFoundException(f"No book found with title {title}.")

            elif (id is not strawberry.UNSET):
                book = BookRepository.get_by(id=id)
                if (book is None):
                    raise BookNotFoundException(f"No book found with id {id}.")

            return book

        except BookNotFoundException as e:
            return BookNotFoundError(id=id, title=title, error=str(e.error))
            

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, book: BookInput) -> Union[BookType, BaseError]:
        try:
            book_added = BookRepository.create(Book(**book.__dict__))
            if (book_added is not None):
                return book_added
            else:
                raise BookNotFoundException(f"Book {book.title} already exists.")
        
        except BookNotFoundException as e:
            return BaseError(error=str(e.error))