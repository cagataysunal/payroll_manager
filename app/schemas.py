from datetime import date
from typing import Optional

from sqlmodel import SQLModel

from app.models import Role


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: Optional[str] = None


class EmployeeCreate(SQLModel):
    email: str
    name: str
    entry_date: date
    age: Optional[int] = None
    pay: float
    role: Role = Role.EMPLOYEE
    password: str


class EmployeeReplace(SQLModel):
    email: str
    name: str
    entry_date: date
    age: Optional[int] = None
    pay: float
    role: Role = Role.EMPLOYEE


class EmployeeUpdate(SQLModel):
    email: Optional[str] = None
    name: Optional[str] = None
    entry_date: Optional[date] = None
    age: Optional[int] = None
    pay: Optional[float] = None
    role: Optional[Role] = None


class EmployeeRead(SQLModel):
    id: int
    email: str
    name: str
    entry_date: date
    age: Optional[int] = None
    pay: float
    role: Role
