from typing import Optional, List, Union
import strawberry

from .repository import BookRepository
from .model import Book
from .exceptions import BookNotFoundException

@strawberry.experimental.pydantic.type(model=Book, all_fields=True)
class BookType:
    pass

@strawberry.input
class BookInput(BookType):
    pass

@strawberry.type
class BookNotFoundError:
    id: Optional[int]
    title: Optional[str]
    error: str

@strawberry.type
class BaseError:
    error: str

# A Union type doesn't work for a List of BookTypes combined with an optional Error object
@strawberry.type
class ListOfBooks():
    books: List[BookType]


# This is one way of defining a Union in Strawberry for GraphQL. The response can be either one of these types.
BookResponse = strawberry.union(
    "BookResponse", [BookType, BookNotFoundError]
)

@strawberry.type
class Query:
    @strawberry.field
    def books(self) -> Union[ListOfBooks, BaseError]:
        try:
            books: List[BookType] = BookRepository.get_all()
            # books = [] # Uncomment this if you want to test having no books!
            if (len(books) > 0):
                return ListOfBooks(books=books)
                
        except BookNotFoundException as e:
            return BaseError(error=str(e))

    @strawberry.field
    def book(self,
        title: Optional[str] = strawberry.UNSET,
        id: Optional[int] = strawberry.UNSET,
    ) -> BookResponse:
        try:
            if (title is not strawberry.UNSET):
                book: BookType = BookRepository.get_by(title)

            elif (id is not strawberry.UNSET):
                book = BookRepository.get(id=id)

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
        
        except BookNotFoundException as e:
            return BaseError(error=str(e.error))