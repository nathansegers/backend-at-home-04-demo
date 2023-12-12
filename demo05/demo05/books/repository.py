from utils import get_uuid
from database import (
    get_database
)
from .exceptions import BookNotFoundException
from models import BaseBook, Book, BookViewModel, DeleteResponse, Author
import traceback
collection = get_database('books')
authors = get_database('authors')

class BookRepository():

    @staticmethod
    def get_by(**kwargs) -> BookViewModel:
        try:
            db_object = collection.find_one(kwargs)
            author = authors.find_one({'id': db_object['author_id']})
            if db_object is not None:
                book_obj = BookViewModel(**db_object)
                book_obj.author = Author(**author)
                return book_obj
            else:
                print(f"No object of type Book was found in the database with that query!")
                return None
        except Exception as e:
            print(f"Error while getting object of type Book in the database.")
            print(e)

    @staticmethod
    def get_many(**kwargs) -> BookViewModel:
        try:
            db_objects = collection.find(kwargs)
            if db_objects is not None:
                books = []
                for book in db_objects:
                    book_obj = BookViewModel(**book)
                    author = authors.find_one({'id': book['author_id']})
                    book_obj.author = Author(**author)
                    books.append(book_obj)
                return books
            else:
                print(f"No object of type Book was found in the database with that query!")
                return None
        except Exception as e:
            print(f"Error while getting object of type Book in the database.")
            print(traceback.format_exc())

    @staticmethod
    def get_all()  -> BookViewModel:
        try:
            # Select all Books and join the Author with it, using SQLAlchemy
            db_objects = collection.find()
            if db_objects is not None:
                # return db_objects
                books = []
                for book in db_objects:
                    book_obj = BookViewModel(**book)
                    author = authors.find_one({'id': book['author_id']})
                    book_obj.author = Author(**author)
                    books.append(book_obj)
                return books
            else:
                print(f"No object of type Book were found in the database!")
                return None
        except Exception as e:
            print(f"Error while getting object of type Book in the database.")
            print(traceback.format_exc())

    @staticmethod
    def create(book: Book) -> BookViewModel:
        try:
            document = book.dict()
            if (BookRepository.get_by(title=document['title'])):
                raise BookNotFoundException(f"Book {book.title} already exists.")
            document["_id"] = get_uuid()
            document["id"] = len(BookRepository.get_all()) + 1
            result = collection.insert_one(document)
            assert result.acknowledged
            return BookRepository.get_by(_id=result.inserted_id)

        except Exception as e:
            print(f"Error while creating object of type Book in the database.")
            print(e)

    @staticmethod
    def update(book: Book) -> BookViewModel:
        """Update an existing book"""
        document = book.dict()
        result = collection.replace_one({"_id": book.id}, document)

        if result.matched_count == 0:
            raise BookNotFoundException(book.id)
        
        return BookRepository.get_by(book.id)

    @staticmethod
    def delete(book: BaseBook) -> DeleteResponse:
        """Delete a book"""
        result = collection.delete_one({"_id": book.id})
        if result.deleted_count == 0:
            raise BookNotFoundException(book.id)
        
        return "Book deleted"