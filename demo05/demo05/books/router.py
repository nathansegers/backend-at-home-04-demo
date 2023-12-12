from fastapi.routing import APIRouter
from fastapi.responses import Response
from fastapi import Depends, Response, status
from typing import List, Union
from models import Book, UpdateBook, DeleteResponse, DeleteBook, BookViewModel
from .repository import BookRepository

router = APIRouter()
repo = BookRepository

@router.post("/", tags=["Books"], name="Create a book", responses={status.HTTP_201_CREATED: {"model": BookViewModel}, status.HTTP_409_CONFLICT: {"model": str}})
def create_book(book: Book, response: Response):
    """
    Create a book and add it to the list of existing books.
    """
    added_book = repo.create(book)
    if (added_book is None):
        response.status_code = status.HTTP_409_CONFLICT
        response.status_message = "Book already exists"
        return response.status_message
    else:
        response.status_code = status.HTTP_201_CREATED
        response.status_message = "Book has been added"
        return added_book

@router.get("/", tags=["Books"], name="Get all books from our database", 
responses={status.HTTP_200_OK: {"model": List[BookViewModel]}, status.HTTP_404_NOT_FOUND: {"model": str}}
)
def get_books(response: Response):
    """
    Get all books.
    """

    books = repo.get_all()
    print(books)

    if (len(books) > 0):
        response.status_code = status.HTTP_200_OK
        return books
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "No books found"

@router.get("/{book_id}", tags=["Books"], name="Get a book", responses={status.HTTP_200_OK: {"model": BookViewModel}, status.HTTP_404_NOT_FOUND: {"model": str}})
def get_book(book_id: int, response: Response):
    """
    Get a book by its id.
    """
    book = repo.get_by(id=book_id)
    # print(book)

    if (book is not None):
        response.status_code = status.HTTP_200_OK
        return book
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "No book found"

@router.put("", tags=["Books"], name="Update a book", responses={status.HTTP_200_OK: {"model": BookViewModel}, status.HTTP_404_NOT_FOUND: {"model": str}})
def update_book(book: UpdateBook, response: Response):
    """
    Update a book by its id.
    """
    book = repo.update(book)
    if (book is not None):
        response.status_code = status.HTTP_200_OK
        return book
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "No book found with that ID"

@router.delete("/{book_id}", tags=["Books"], name="Delete a book", responses={status.HTTP_200_OK: {"model": DeleteResponse}, status.HTTP_404_NOT_FOUND: {"model": str}})
def delete_book(book_id: int, response: Response):
    """
    Update a book by its id.
    """
    book = repo.delete(DeleteBook(id=book_id))
    if (book > 0):
        response.status_code = status.HTTP_200_OK
        return DeleteResponse(message="Book has been deleted successfully!")
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "No books found"