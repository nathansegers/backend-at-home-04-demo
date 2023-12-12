from database import (
    Base,
    db # db is our database connector
)
from .model import Book as BookModel

from sqlalchemy import Column, String, Text, Integer


class Book(Base, dict):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    author = Column(String(255))
    year = Column(Integer)
    publisher = Column(String(255))
    description = Column(Text)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = BookModel
        self.schema = self.__class__

    def get_by(self, **kwargs):
        try:
            # title="The Great Gatsby"
            # author="F. Scott Fitzgerald"
            # db.query(Book).filter_by(title="The Great Gatsby", author="F. Scott Fitzgerald").first()
            db_object = db.query(self.schema).filter_by(**kwargs).first()
            if db_object is not None:
                return self.model.from_orm(db_object)
            else:
                print(f"No object of type {self.schema} was found in the database with that query!")
                return None
        except Exception as e:
            print(f"Error while getting object of type {self.schema} in the database.")
            print(e)
            db.rollback()

    def get_many(self, **kwargs):
        try:
            db_objects = db.query(self.schema).filter_by(**kwargs).all()
            if db_objects is not None:
                return list(map(lambda x: self.model.from_orm(x), db_objects))
            else:
                print(f"No object of type {self.schema} was found in the database with that query!")
                return None
        except Exception as e:
            print(f"Error while getting object of type {self.schema} in the database.")
            print(e)
            db.rollback()

    def get_all(self):
        try:
            db_objects = db.query(self.schema).all()
            if db_objects:
                return list(map(lambda x: self.model.from_orm(x), db_objects))
            else:
                print(f"No object of type {self.schema} were found in the database!")
                return None
        except Exception as e:
            print(f"Error while getting object of type {self.schema} in the database.")
            print(e)
            db.rollback()

    def create(self, obj):
        try:
            obj_in_db = self.get_by(title=obj.title)
            if obj_in_db is None:
                print(f"No object of type {self.schema} were found in the database with that title!")

                new_obj = self.schema(**obj.dict())
                db.add(new_obj)
                db.commit()

                print(f"{self.model} has been added to the database!")
                obj = self.model.from_orm(new_obj)
            else:
                obj = None
                print(f"A {self.model} already exists.")

            return obj

        except Exception as e:
            print(f"Error while creating object of type {self.schema} in the database.")
            print("Rolling back the database commit.")
            print(e)
            db.rollback()

    def update(self, new_obj):
        try:
            old_obj = db.query(self.schema).filter_by(id=new_obj.id).first()

            for key, value in new_obj.dict(exclude_unset=True).items():
                if getattr(old_obj, key) != value: ## difference
                    setattr(old_obj, key, value)
                    
            db.commit()
            updated_object = self.model.from_orm(old_obj)
            return updated_object

        except Exception as e:
            print(f"Error while updating object of type {self.schema} in the database.")
            print(e)
            print("Rolling back the database commit.")
            db.rollback()

    
    def delete(self, old_obj):
        try:
            num_rows_deleted = db.query(self.schema).filter_by(id=old_obj.id).delete()
            print(f"Deleted {num_rows_deleted} items.")
            db.commit()
            return num_rows_deleted
        except Exception as e:
            print(f"Error while deleting object of type {self.schema} from the database.")
            print(e)
            print("Rolling back the database commit.")
            db.rollback()