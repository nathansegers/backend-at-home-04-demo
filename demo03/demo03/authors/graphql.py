from typing import Optional, List, Union
import strawberry

from .exceptions import AuthorNotFoundException
from shared import BaseError
from graphql_models import AuthorInput, AuthorNotFoundError, ListOfAuthors, AuthorType, AuthorResponse
from models import Author
from .repository import AuthorRepository

@strawberry.type
class Query:
    @strawberry.field
    def authors(self) -> Union[ListOfAuthors, BaseError]:
        try:
            authors: List[AuthorType] = AuthorRepository.get_all()
            # authors = [] # Uncomment this if you want to test having no authors!
            if (len(authors) > 0):
                return ListOfAuthors(authors=authors)
            else:
                raise AuthorNotFoundException(f"No authors found")
                
        except AuthorNotFoundException as e:
            return BaseError(error=str(e))

    @strawberry.field
    def author(self,
        name: Optional[str] = strawberry.UNSET,
        id: Optional[int] = strawberry.UNSET,
    ) -> AuthorResponse:
        try:
            if (name is not strawberry.UNSET):
                author: AuthorType = AuthorRepository.get_by(name=name)
                if (author is None):
                    raise AuthorNotFoundException(f"No author found with name {name}.")

            elif (id is not strawberry.UNSET):
                author = AuthorRepository.get_by(id=id)
                if (author is None):
                    raise AuthorNotFoundException(f"No author found with id {id}.")

            return author

        except AuthorNotFoundException as e:
            return AuthorNotFoundError(id=id, name=name, error=str(e.error))
            

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_author(self, author: AuthorInput) -> Union[AuthorType, BaseError]:
        try:
            author_added = AuthorRepository.create(Author(**author.__dict__))
            if (author_added is not None):
                return author_added
            else:
                raise AuthorNotFoundException(f"Author {author.name} already exists.")
        
        except AuthorNotFoundException as e:
            return BaseError(error=str(e.error))