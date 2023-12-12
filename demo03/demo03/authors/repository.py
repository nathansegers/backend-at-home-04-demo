from models import AuthorViewModel
from database import (
    Base,
    db # db is our database connector
)
from authors.schema import AuthorTable

class AuthorRepository():

    @staticmethod
    def get_by(**kwargs):
        try:
            db_object = db.query(AuthorTable).filter_by(**kwargs).first()
            if db_object is not None:
                return AuthorViewModel.from_orm(db_object)
            else:
                print(f"No object of type {AuthorTable} was found in the database with that query!")
                return None
        except Exception as e:
            print(f"Error while getting object of type {AuthorTable} in the database.")
            print(e)
            db.rollback()

    @staticmethod
    def get_many(**kwargs):
        try:
            db_objects = db.query(AuthorTable).filter_by(**kwargs).all()
            if db_objects is not None:
                return list(map(lambda x: AuthorViewModel.from_orm(x), db_objects))
            else:
                print(f"No object of type {AuthorTable} was found in the database with that query!")
                return None
        except Exception as e:
            print(f"Error while getting object of type {AuthorTable} in the database.")
            print(e)
            db.rollback()

    @staticmethod
    def get_all():
        try:
            # Select all Authors and join the Author with it, using SQLAlchemy
            db_objects = db.query(AuthorTable).all()
            if db_objects:
                # return db_objects
                return list(map(lambda x: AuthorViewModel.from_orm(x), db_objects))
            else:
                print(f"No object of type {AuthorTable} were found in the database!")
                return None
        except Exception as e:
            print(f"Error while getting object of type {AuthorTable} in the database.")
            print(e)
            db.rollback()

    @staticmethod
    def create(obj):
        try:
            obj_in_db = AuthorRepository.get_by(title=obj.title)
            if obj_in_db is None:
                print(f"No object of type {AuthorTable} were found in the database with that title!")

                new_obj = AuthorTable(**obj.dict())
                db.add(new_obj)
                db.commit()

                print(f"{AuthorViewModel} has been added to the database!")
                obj = AuthorViewModel.from_orm(new_obj)
            else:
                obj = None
                print(f"A {AuthorViewModel} already exists.")

            return obj

        except Exception as e:
            print(f"Error while creating object of type {AuthorTable} in the database.")
            print("Rolling back the database commit.")
            print(e)
            db.rollback()

    @staticmethod
    def update(new_obj):
        try:
            old_obj = db.query(AuthorTable).filter_by(id=new_obj.id).first()

            for key, value in new_obj.dict(exclude_unset=True).items():
                if getattr(old_obj, key) != value: ## difference
                    setattr(old_obj, key, value)
                    
            db.commit()
            updated_object = AuthorViewModel.from_orm(old_obj)
            return updated_object

        except Exception as e:
            print(f"Error while updating object of type {AuthorTable} in the database.")
            print(e)
            print("Rolling back the database commit.")
            db.rollback()

    @staticmethod
    def delete(old_obj):
        try:
            num_rows_deleted = db.query(AuthorTable).filter_by(id=old_obj.id).delete()
            print(f"Deleted {num_rows_deleted} items.")
            db.commit()
            return num_rows_deleted
        except Exception as e:
            print(f"Error while deleting object of type {AuthorTable} from the database.")
            print(e)
            print("Rolling back the database commit.")
            db.rollback()