
class AuthorNotFoundException(Exception):
    def __init__(self, error = '', *args, **kwargs):
        self.error = error

    def __str__(self):
        return self.error