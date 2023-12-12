# Demo05 -- Databases with MongoDB

In this demonstration, we will be using a MongoDB database that has a relationship between two collections. The first collection is a list of books, and the second collection is a list of authors. The books are related to the authors by the authors's ID.

Use these books as an example
```json
[
    {
        "title": "Harry Potter and the Chamber of Secrets",
        "year": 1998,
        "publisher": {
            "name": "Bloomsbury",
            "location": "London, England"
        },
        "description": "Harry Potter and the Chamber of Secrets is a fantasy novel written by British author J. K. Rowling.",
        "author": {
            "name": "J.K. Rowling",
        },
    },

    {
        "title": "The Hobbit",
        "author_id": 2,
        "year": 1937,
        "publisher": "Allen & Unwin",
        "description": "The Hobbit, or There and Back Again is a children's fantasy novel by English author J. R. R. Tolkien."
    },

    {
        "title": "The Little Prince",
        "author_id": 3,
        "year": 1943,
        "publisher": "Reynal & Hitchcock",
        "description": "The Little Prince is a novella, the most famous work of French aristocrat, writer, poet, and pioneering aviator Antoine de Saint-Exupéry."
    }
]
```

Use these authors as an example
```json
[
    {
        "name": "J.K. Rowling",
        "birthdate": "1965-07-31 00:00:00",
        "gender": "Female"
    },

    {
        "name": "J.R.R. Tolkien",
        "birthdate": "1892-01-03 00:00:00",
        "gender": "Male"
    },
    
    {
        "name": "Antoine de Saint-Exupéry",
        "birthdate": "1900-06-29 00:00:00",
        "gender": "Male"
    }
]
```