from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.db import SessionDep
from app.models import Employee, Role
from app.schemas import (
    EmployeeCreate,
    EmployeeRead,
    EmployeeReplace,
    EmployeeUpdate,
)
from app.security import get_current_employee, hash_password, require_roles

router = APIRouter()


@router.post("/employee", response_model=EmployeeRead)
async def create_employee(
    employee: EmployeeCreate,
    session: SessionDep,
    _: Employee = Depends(require_roles(Role.ADMIN, Role.MANAGER)),
) -> EmployeeRead:
    employee_data = employee.model_dump(exclude={"password"})
    db_employee = Employee(
        **employee_data,
        hashed_password=hash_password(employee.password),
    )
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return EmployeeRead.model_validate(db_employee, from_attributes=True)


@router.get("/employees", response_model=list[EmployeeRead])
def list_employees(
    session: SessionDep,
    _: Employee = Depends(get_current_employee),
) -> list[EmployeeRead]:
    employees = session.exec(select(Employee)).all()
    return [
        EmployeeRead.model_validate(employee, from_attributes=True)
        for employee in employees
    ]


@router.get("/employee/{employee_id}", response_model=EmployeeRead)
def get_employee(
    employee_id: int,
    session: SessionDep,
    _: Employee = Depends(get_current_employee),
) -> EmployeeRead:
    employee = session.exec(
        select(Employee).where(Employee.id == employee_id)
    ).one_or_none()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return EmployeeRead.model_validate(employee, from_attributes=True)


@router.put("/employee/{employee_id}", response_model=EmployeeRead)
def replace_employee(
    employee_id: int,
    employee_update: EmployeeReplace,
    session: SessionDep,
    _: Employee = Depends(require_roles(Role.ADMIN, Role.MANAGER)),
) -> EmployeeRead:
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
    return EmployeeRead.model_validate(employee, from_attributes=True)


@router.patch("/employee/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    session: SessionDep,
    _: Employee = Depends(require_roles(Role.ADMIN, Role.MANAGER)),
) -> EmployeeRead:
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
    return EmployeeRead.model_validate(employee, from_attributes=True)


@router.delete("/employee/{employee_id}", status_code=204)
def delete_employee(
    employee_id: int,
    session: SessionDep,
    _: Employee = Depends(require_roles(Role.ADMIN)),
) -> None:
    employee = session.exec(
        select(Employee).where(Employee.id == employee_id)
    ).one_or_none()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    session.delete(employee)
    session.commit()
    return None
