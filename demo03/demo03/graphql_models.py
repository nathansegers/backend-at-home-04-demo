from typing import Optional, List, Union
import strawberry
from models import Book, Author, BookViewModel, AuthorViewModel
from shared import BaseError

# Graphql Models

# Books

@strawberry.experimental.pydantic.type(model=Book, all_fields=True)
class BookType:
    pass

@strawberry.experimental.pydantic.type(model=Author, all_fields=True)
class AuthorType:
    pass

@strawberry.experimental.pydantic.type(model=BookViewModel, fields=['id', 'title', 'year', 'publisher', 'description'])
class BookViewModelType:
    author: AuthorType

@strawberry.experimental.pydantic.type(model=AuthorViewModel, fields=['id', 'name', 'birthdate', 'gender'])
class AuthorViewModelType:
    books: List[BookType]

# As an Input type, we need to provide all the fields of the BookType object, which means we only fill in the author_id
@strawberry.input
class BookInput(BookType):
    pass

@strawberry.input
class AuthorInput(AuthorType):
    pass

# --- ErrorTypes ---

@strawberry.type
class BookNotFoundError:
    id: Optional[int]
    title: Optional[str]
    error: str

@strawberry.type
class AuthorNotFoundError:
    id: Optional[int]
    name: Optional[str]
    error: str

# --- UnionTypes ---

# A Union type doesn't work for a List of BookTypes combined with an optional Error object, so we need to be creative!
@strawberry.type
class ListOfBooks():
    books: List[BookViewModelType]

# A Union type doesn't work for a List of AuthorTypes combined with an optional Error object
@strawberry.type
class ListOfAuthors():
    authors: List[AuthorViewModelType]


# This is one way of defining a Union in Strawberry for GraphQL. The response can be either one of these types.
BookResponse = strawberry.union(
    "BookResponse", [BookType, BookNotFoundError]
)

# This is one way of defining a Union in Strawberry for GraphQL. The response can be either one of these types.
AuthorResponse = strawberry.union(
    "AuthorResponse", [AuthorType, AuthorNotFoundError]
)





