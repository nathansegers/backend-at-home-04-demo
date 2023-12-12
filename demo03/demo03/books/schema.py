from typing import List, Optional
from datetime import datetime

from database import (
    Base,
    db # db is our database connector
)
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class BookTable(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    year = Column(Integer)
    publisher = Column(String(255))
    description = Column(Text)

    author_id = Column(Integer, ForeignKey("authors.id"))
    # Relationship with Author on the `books.author_id` == `authors.id`
    author = relationship(
        "AuthorTable",
        back_populates="books",
        primaryjoin="BookTable.author_id==AuthorTable.id"
    )