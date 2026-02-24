from collections.abc import Generator
from typing import Annotated, Any

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

POSTGRESQL_DB_NAME = "payroll_manager"
POSTGRESQL_URL = f"postgresql://localhost/{POSTGRESQL_DB_NAME}"

engine = create_engine(POSTGRESQL_URL)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, Any, Any]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
