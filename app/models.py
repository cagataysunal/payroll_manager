from datetime import date
from enum import Enum

import sqlalchemy as sa
from sqlmodel import Field, SQLModel


class Role(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class EmployeeBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    entry_date: date
    age: int | None = Field(default=None, index=True)
    pay: float = Field(ge=0)
    role: Role = Field(
        default=Role.EMPLOYEE,
        sa_column=sa.Column(
            sa.Enum(
                Role,
                name="role",
                values_callable=lambda enum: [item.value for item in enum],
            )
        ),
    )


class Employee(EmployeeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
