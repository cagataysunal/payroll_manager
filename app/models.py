from datetime import date

from sqlmodel import Field, SQLModel


class Employee(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    entry_date: date
    age: int | None = Field(default=None, index=True)
    pay: float
