import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import select

from app.db import SessionDep
from app.models import Employee, Role
from app.schemas import TokenData

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_employee(
    session: SessionDep,
    email: str,
    password: str,
) -> Employee | None:
    employee = session.exec(
        select(Employee).where(Employee.email == email)
    ).one_or_none()
    if employee is None:
        return None
    if not verify_password(password, employee.hashed_password):
        return None
    return employee


def create_access_token(
    data: dict[str, object],
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_employee(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> Employee:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        token_data = TokenData(email=email)
    except JWTError as exc:
        raise credentials_exception from exc
    if token_data.email is None:
        raise credentials_exception
    employee = session.exec(
        select(Employee).where(Employee.email == token_data.email)
    ).one_or_none()
    if employee is None:
        raise credentials_exception
    return employee


def require_roles(*roles: Role):
    def role_dependency(employee: Employee = Depends(get_current_employee)) -> Employee:
        if roles and employee.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return employee

    return role_dependency
