from sqlalchemy import Column, Integer, String, Text, Boolean
from database.base import BASE


class ToDo(BASE):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    completed = Column(Boolean)

    def __str__(self):
        return f"{self.title} - {self.description}"