from sqlmodel import Field
from typing import Optional
from uuid import UUID, uuid4
from base import BASE, engine

class Reader(BASE, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    has_books: bool = False

BASE.metadata.create_all(engine)