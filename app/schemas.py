from datetime import date
from typing import Optional

from sqlmodel import SQLModel


class EmployeeCreate(SQLModel):
    name: str
    entry_date: date
    age: Optional[int] = None
    pay: float


class EmployeeReplace(SQLModel):
    name: str
    entry_date: date
    age: Optional[int] = None
    pay: float


class EmployeeUpdate(SQLModel):
    name: Optional[str] = None
    entry_date: Optional[date] = None
    age: Optional[int] = None
    pay: Optional[float] = None
