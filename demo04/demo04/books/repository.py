from utils import get_uuid
from database import (
    get_database # db is our database connector
)
from .model import Book
from .exceptions import BookNotFoundException

collection = get_database("books")

class BookRepository:
    
    @staticmethod
    def get(book_id: str) -> Book:
        """Retrieve a single Book by its unique id"""
        document = collection.find_one({"_id": book_id})
        if not document:
            raise BookNotFoundException(book_id)
        return Book(**document)

    @staticmethod
    def get_by(title: str) -> Book:
        """Retrieve a single Book by its unique id"""
        document = collection.find_one({"title": title})
        if not document:
            raise BookNotFoundException(title)
        return Book(**document)

    @staticmethod
    def get_all() -> list[Book]:
        """Retrieve all books"""
        return [Book(**document) for document in collection.find()]

    @staticmethod
    def create(book: Book) -> Book:
        """Create a new book"""
        document = book.dict()
        document["_id"] = get_uuid()
        document["id"] = len(BookRepository.get_all()) + 1
        result = collection.insert_one(document)
        assert result.acknowledged
        return BookRepository.get(result.inserted_id)

    @staticmethod
    def update(book: Book) -> Book:
        """Update an existing book"""
        document = book.dict()
        result = collection.replace_one({"_id": book.id}, document)

        if result.matched_count == 0:
            raise BookNotFoundException(book.id)
        
        return BookRepository.get(book.id)

    @staticmethod
    def delete(book_id: str) -> None:
        """Delete a book"""
        result = collection.delete_one({"_id": book_id})
        if result.deleted_count == 0:
            raise BookNotFoundException(book_id)
        
        return "Book deleted"