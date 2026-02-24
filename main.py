import datetime
from collections.abc import Generator
from contextlib import asynccontextmanager
from enum import Enum
from typing import Annotated, Any, AsyncGenerator, Optional

from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

postgresql_db_name = "payroll_manager"
postgresql_url = f"postgresql://localhost/{postgresql_db_name}"

engine = create_engine(postgresql_url)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, Any, Any]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


class Role(Enum):
    ADMIN = 1
    USER = 2


class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    entry_date: datetime.date
    age: Optional[int] = Field(default=None, index=True)
    pay: float


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/employee")
def create_employee(employee: Employee, session: SessionDep) -> Employee:
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee


@app.get("/employees")
def list_employees(session: SessionDep) -> list[Employee]:
    employees = session.exec(select(Employee)).all()
    return list(employees)
