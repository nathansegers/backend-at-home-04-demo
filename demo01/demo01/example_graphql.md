
Fetching one book which can either return a BookType of a BookNotFoundError

```graphql
{
  book(title: "The Hobbit") {
    ... on BookType {
      title
      id
    }
    ... on BookNotFoundError {
      error
    }
  }
}
```