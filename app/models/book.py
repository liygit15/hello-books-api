# app/models/book.py
# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Fictional Book", "A fantasy novel set in an imaginary world."),
#     Book(2, "Wheel of Time", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ]

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional, TYPE_CHECKING
from ..db import db

if TYPE_CHECKING:
    from .author import Author

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Optional["Author"]] = relationship(back_populates="books")


    @classmethod
    def from_dict(cls, book_data):
        author_id = book_data.get("author_id")
        new_book = Book(title=book_data["title"],
                        description=book_data["description"],
                        author_id=author_id)
        return new_book
    
    
    def to_dict(self):
        book_as_dict = {}
        book_as_dict["id"] = self.id
        book_as_dict["title"] = self.title
        book_as_dict["description"] = self.description

        if self.author:
            book_as_dict["author"] = self.author.name

        return book_as_dict

