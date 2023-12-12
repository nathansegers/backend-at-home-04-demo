from fastapi.routing import APIRouter
from fastapi.responses import Response
from fastapi import Depends, Response, status
from typing import List, Union
from .model import Book, UpdateBook, DeleteBookResponse, DeleteBook
from .schema import Book as DBBook

async def get_db() -> DBBook:
    from database import db
    try:
        conn = DBBook()
        yield conn
    finally:
        db.close()
router = APIRouter()

@router.post("/", tags=["Books"], name="Create a book", responses={status.HTTP_201_CREATED: {"model": Book}, status.HTTP_409_CONFLICT: {"model": str}})
def create_book(book: Book, response: Response, db = Depends(get_db)):
    """
    Create a book and add it to the list of existing books.
    """
    added_book = db.create(book)
    if (added_book is None):
        response.status_code = status.HTTP_409_CONFLICT
        response.status_message = "Book already exists"
        return response.status_message
    else:
        response.status_code = status.HTTP_201_CREATED
        response.status_message = "Book has been added"
        return added_book

@router.get("/", tags=["Books"], name="Get all books from our database", responses={status.HTTP_200_OK: {"model": List[Book]}, status.HTTP_404_NOT_FOUND: {"model": str}})
def get_books(response: Response, db: DBBook = Depends(get_db)):
    """
    Get all books.
    """

    books = db.get_all()
    # print(books)

    if (len(books) > 0):
        response.status_code = status.HTTP_200_OK
        return books
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "No books found"

@router.get("/{book_id}", tags=["Books"], name="Get a book", responses={status.HTTP_200_OK: {"model": Book}, status.HTTP_404_NOT_FOUND: {"model": str}})
def get_book(book_id: int, response: Response, db: DBBook = Depends(get_db)):
    """
    Get a book by its id.
    """
    book = db.get_by(id=book_id)
    # print(book)

    if (book is not None):
        response.status_code = status.HTTP_200_OK
        return book
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "No book found"

@router.put("", tags=["Books"], name="Update a book", responses={status.HTTP_200_OK: {"model": Book}, status.HTTP_404_NOT_FOUND: {"model": str}})
def update_book(book: UpdateBook, response: Response, db: DBBook = Depends(get_db)):
    """
    Update a book by its id.
    """
    book = db.update(book)
    if (book is not None):
        response.status_code = status.HTTP_200_OK
        return book
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "No book found with that ID"

@router.delete("/{book_id}", tags=["Books"], name="Delete a book", responses={status.HTTP_200_OK: {"model": DeleteBookResponse}, status.HTTP_404_NOT_FOUND: {"model": str}})
def delete_book(book_id: int, response: Response, db: DBBook = Depends(get_db)):
    """
    Update a book by its id.
    """
    book = db.delete(DeleteBook(id=book_id))
    if (book > 0):
        response.status_code = status.HTTP_200_OK
        return DeleteBookResponse(message="Book has been deleted successfully!")
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "No books found"