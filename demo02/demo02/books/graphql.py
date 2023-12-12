from typing import Optional, List, Union
import strawberry

from .schema import Book as DBBook
from .model import Book
from .exceptions import BookNotFoundException
conn = DBBook()

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
            books: List[BookType] = conn.get_all()
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
                book: BookType = conn.get_by(title=title)
                if (book is None):
                    raise BookNotFoundException(f"No book found with title {title}.")

            elif (id is not strawberry.UNSET):
                book = conn.get_by(id=id)
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
            book_added = conn.create(Book(**book.__dict__))
            if (book_added is not None):
                return book_added
            else:
                raise BookNotFoundException(f"Book {book.title} already exists.")
        
        except BookNotFoundException as e:
            return BaseError(error=str(e.error))