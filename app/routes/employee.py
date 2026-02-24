from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.db import SessionDep
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeReplace, EmployeeUpdate

router = APIRouter()


@router.post("/employee")
async def create_employee(
    employee: EmployeeCreate,
    session: SessionDep,
) -> Employee:
    db_employee = Employee(**employee.model_dump())
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee


@router.get("/employees")
def list_employees(session: SessionDep) -> list[Employee]:
    employees = session.exec(select(Employee)).all()
    return list(employees)


@router.get("/employee/{employee_id}")
def get_employee(employee_id: int, session: SessionDep) -> Employee:
    employee = session.exec(
        select(Employee).where(Employee.id == employee_id)
    ).one_or_none()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return employee


@router.put("/employee/{employee_id}")
def replace_employee(
    employee_id: int,
    employee_update: EmployeeReplace,
    session: SessionDep,
) -> Employee:
    employee = session.exec(
        select(Employee).where(Employee.id == employee_id)
    ).one_or_none()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    update_data = employee_update.model_dump()
    for key, value in update_data.items():
        setattr(employee, key, value)
    session.commit()
    session.refresh(employee)
    return employee


@router.patch("/employee/{employee_id}")
def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    session: SessionDep,
) -> Employee:
    employee = session.exec(
        select(Employee).where(Employee.id == employee_id)
    ).one_or_none()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    update_data = employee_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee, key, value)
    session.commit()
    session.refresh(employee)
    return employee


@router.delete("/employee/{employee_id}", status_code=204)
def delete_employee(employee_id: int, session: SessionDep) -> None:
    employee = session.exec(
        select(Employee).where(Employee.id == employee_id)
    ).one_or_none()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    session.delete(employee)
    session.commit()
    return None
