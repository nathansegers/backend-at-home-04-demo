import strawberry

@strawberry.type
class BaseError:
    error: str

    