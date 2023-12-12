```graphql

query {
  
  books {
    ... on ListOfBooks {
      books {
        title
        id
        author {
          name
          id
          gender
        }
      }
      
    }
    ... on BaseError {
      error
    }
  }

}

```