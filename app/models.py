from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    entry_date: date
    age: Optional[int] = Field(default=None, index=True)
    pay: float
