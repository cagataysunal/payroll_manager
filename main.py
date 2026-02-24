import datetime
from collections.abc import Generator
from contextlib import asynccontextmanager
from typing import Annotated, Any, AsyncGenerator, Optional

from fastapi import Depends, FastAPI, HTTPException, status
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


class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    entry_date: datetime.date
    age: Optional[int] = Field(default=None, index=True)
    pay: float


class EmployeeCreate(SQLModel):
    name: str
    entry_date: datetime.date
    age: Optional[int] = None
    pay: float


class EmployeeReplace(SQLModel):
    name: str
    entry_date: datetime.date
    age: Optional[int] = None
    pay: float


class EmployeeUpdate(SQLModel):
    name: Optional[str] = None
    entry_date: Optional[datetime.date] = None
    age: Optional[int] = None
    pay: Optional[float] = None


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/employee")
async def create_employee(
    employee: EmployeeCreate,
    session: SessionDep,
) -> Employee:
    db_employee = Employee(**employee.model_dump())
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee


@app.delete("/employee/{employee_id}", status_code=204)
def delete_employee(id: int, session: SessionDep) -> None:
    employee = session.exec(select(Employee).where(Employee.id == id)).one_or_none()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    session.delete(employee)
    session.commit()
    return None


@app.get("/employee/{employee_id}")
def get_employee(id: int, session: SessionDep) -> Employee:
    employee = session.exec(select(Employee).where(Employee.id == id)).one_or_none()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return employee


@app.put("/employee/{employee_id}")
def replace_employee(
    id: int,
    employee_update: EmployeeReplace,
    session: SessionDep,
) -> Employee:
    employee = session.exec(select(Employee).where(Employee.id == id)).one_or_none()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    update_data = employee_update.model_dump()
    for key, value in update_data.items():
        setattr(employee, key, value)
    session.commit()
    session.refresh(employee)
    return employee


@app.patch("/employee/{employee_id}")
def update_employee(
    id: int,
    employee_update: EmployeeUpdate,
    session: SessionDep,
) -> Employee:
    employee = session.exec(select(Employee).where(Employee.id == id)).one_or_none()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    update_data = employee_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee, key, value)
    session.commit()
    session.refresh(employee)
    return employee


@app.get("/employees")
def list_employees(session: SessionDep) -> list[Employee]:
    employees = session.exec(select(Employee)).all()
    return list(employees)
