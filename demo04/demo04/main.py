from typing import List, Optional
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

from books.graphql import Query as BooksQuery, Mutation as BooksMutation
from books.router import router as books_router

# Import and start the database connection!
import database as db

@strawberry.type
class Query(BooksQuery):
    pass

@strawberry.type
class Mutation(BooksMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI(
    title="FastAPI Demo for Backend@Home",
    description="This is a demo of FastAPI",
    version="0.0.1",
)

app.include_router(graphql_app, prefix="/graphql")

app.include_router(books_router, prefix="/books")

if __name__ == "__main__":
    # Run the app with uvicorn and autoreload
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)