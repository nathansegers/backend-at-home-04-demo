
class BookNotFoundException(Exception):
    def __init__(self, id = '', error = '', *args, **kwargs):
        self.error = f"Book was not found with id {id}" if id else error

    def __str__(self):
        return self.error