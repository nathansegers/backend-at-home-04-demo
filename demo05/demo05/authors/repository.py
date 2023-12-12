from utils import get_uuid
from database import (
    get_database
)
from .exceptions import AuthorAlreadyExist, AuthorNotFoundException
from models import BaseAuthor, Author, AuthorViewModel, DeleteResponse, Book
import traceback

collection = get_database('authors')
books = get_database('books')

class AuthorRepository():

    @staticmethod
    def get_by(**kwargs) -> AuthorViewModel:
        try:
            db_object = collection.find_one(kwargs)
            books = books.find({'author_id': db_object['id']})
            db_object['books'] = books
            if db_object is not None:
                return AuthorViewModel(**db_object)
            else:
                print(f"No object of type Author was found in the database with that query!")
                return None
        except Exception as e:
            print(f"Error while trying to get one of the database objects.")
            print(traceback.format_exc())

    @staticmethod
    def get_many(**kwargs) -> AuthorViewModel:
        try:
            db_objects = collection.find(kwargs)
            if db_objects is not None:
                authors = []
                for author in db_objects:
                    author_obj = AuthorViewModel(**author)
                    author_books = books.find({'author_id': author['id']})
                    author_obj.books = [Book(**book) for book in author_books]
                    authors.append(author_obj)
            else:
                print(f"No object of type Author was found in the database with that query!")
                return None
        except Exception as e:
            print(f"Error while trying to get database objects in the Authors collection.")
            print(traceback.format_exc())

    @staticmethod
    def get_all() -> AuthorViewModel:
        try:
            # Select all Authors and join the Author with it, using SQLAlchemy
            db_objects = collection.find()
            if db_objects is not None:
                authors = []
                for author in db_objects:
                    author_obj = AuthorViewModel(**author)
                    author_books = books.find({'author_id': author['id']})
                    author_obj.books = [Book(**book) for book in author_books]
                    authors.append(author_obj)
                return authors
            else:
                print(f"No object of type Author were found in the database!")
                return []
        except Exception as e:
            print(f"Error while trying to fetch all the Authors.")
            print(traceback.format_exc())

    @staticmethod
    def create(author: Author) -> AuthorViewModel:
        try:
            document = author.dict()
            if (AuthorRepository.get_by(name=document['name'])):
                raise AuthorAlreadyExist(f"Author {author.name} already exists.")
            document['_id'] = get_uuid()
            document['id'] = len(AuthorRepository.get_all()) + 1
            result = collection.insert_one(document)
            assert result.acknowledged
            return AuthorRepository.get_by(_id=result.inserted_id)

        except Exception as e:
            print(f"Error while creating object of type Author in the database.")
            print(e)

    @staticmethod
    def update(author: Author) -> AuthorViewModel:
        """Update an existing author"""
        document = author.dict()
        result = collection.replace_one({"_id": author.id}, document)

        if result.matched_count == 0:
            raise AuthorNotFoundException(author.id)
        
        return AuthorRepository.get_by(author.id)

    @staticmethod
    def delete(author: BaseAuthor) -> DeleteResponse:
        """Delete an author"""
        result = collection.delete_one({"_id": author.id})
        if result.deleted_count == 0:
            raise AuthorNotFoundException(author.id)
        
        return "Author deleted"