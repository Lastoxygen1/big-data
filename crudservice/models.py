from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4

class Reader(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    has_books: bool = False