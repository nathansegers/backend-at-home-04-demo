from typing import List, Optional
from datetime import datetime

from database import (
    Base,
    db # db is our database connector
)
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class AuthorTable(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    birthdate = Column(DateTime)
    gender = Column(String(255))

    books = relationship("BookTable", back_populates="author")