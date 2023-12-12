from fastapi.routing import APIRouter
from fastapi.responses import Response
from fastapi import Depends, Response, status
from typing import List, Union
from models import Author, Gender, DeleteAuthor, DeleteResponse, AuthorViewModel
from .repository import AuthorRepository

router = APIRouter()

repo = AuthorRepository

@router.post("/", tags=["Authors"], name="Create a author", responses={status.HTTP_201_CREATED: {"model": AuthorViewModel}, status.HTTP_409_CONFLICT: {"model": str}})
def create_author(author: Author, response: Response):
    """
    Create a author and add it to the list of existing authors.
    """
    added_author = repo.create(author)
    if (added_author is None):
        response.status_code = status.HTTP_409_CONFLICT
        response.status_message = "Author already exists"
        return response.status_message
    else:
        response.status_code = status.HTTP_201_CREATED
        response.status_message = "Author has been added"
        return added_author

@router.get("/", tags=["Authors"], name="Get all authors from our database", responses={status.HTTP_200_OK: {"model": List[AuthorViewModel]}, status.HTTP_404_NOT_FOUND: {"model": str}})
def get_authors(response: Response):
    """
    Get all authors.
    """

    authors = repo.get_all()
    # print(authors)

    if (len(authors) > 0):
        response.status_code = status.HTTP_200_OK
        return authors
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "No authors found"

@router.get("/{author_id}", tags=["Authors"], name="Get a author", responses={status.HTTP_200_OK: {"model": AuthorViewModel}, status.HTTP_404_NOT_FOUND: {"model": str}})
def get_author(author_id: int, response: Response):
    """
    Get a author by its id.
    """
    author = repo.get_by(id=author_id)
    # print(author)

    if (author is not None):
        response.status_code = status.HTTP_200_OK
        return author
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "No author found"

@router.delete("/{author_id}", tags=["Authors"], name="Delete a author", responses={status.HTTP_200_OK: {"model": DeleteResponse}, status.HTTP_404_NOT_FOUND: {"model": str}})
def delete_author(author_id: int, response: Response):
    """
    Update a author by its id.
    """
    author = repo.delete(DeleteAuthor(id=author_id))
    if (author > 0):
        response.status_code = status.HTTP_200_OK
        return DeleteResponse(message="Author has been deleted successfully!")
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "No authors found"