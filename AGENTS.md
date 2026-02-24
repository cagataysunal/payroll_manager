# Agent Guidelines for Payroll Manager

This document provides guidelines for AI agents working on this codebase.

## Project Overview

- **Framework**: FastAPI
- **Python Version**: 3.14
- **Package Manager**: pip/venv
- **Linter**: Ruff
- **Type Checker**: Pyright (strict mode)
- **Test Framework**: pytest

---

## Commands

### Virtual Environment

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Application

```bash
uvicorn main:app --reload
# or
python -m uvicorn main:app --reload
```

### Linting

```bash
ruff check .
ruff check . --fix
```

### Type Checking

```bash
pyright
# or
python -m pyright
```

### Testing

```bash
pytest                     # Run all tests
pytest -v                  # Verbose output
pytest tests/test_app.py   # Single test file
pytest tests/test_app.py::test_openapi  # Single test function
pytest -k "test_openapi"   # Tests matching pattern
pytest --cov=. --cov-report=term-missing  # With coverage
```

### Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

---

## Code Style Guidelines

### General

- **Line Length**: 88 characters
- **Python Version**: 3.14+
- **No Comments**: Do NOT add comments unless explicitly requested
- **Type Hints**: Always use type hints (strict mode in pyright)

### Imports

- **Order**: Standard library → Third-party → Local application
- Use absolute imports (e.g., `from main import app`)
- Never use wildcard imports (`from module import *`)

### Formatting

- Use Ruff for formatting (`ruff format .`)
- Do not manually format

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | snake_case | `user_name` |
| Functions | snake_case | `def calculate_pay()` |
| Classes | PascalCase | `class UserModel` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY` |
| Modules | snake_case | `user_service.py` |

### Type Annotations

- Always use explicit type hints for function parameters and return types
- Use `Optional[X]` instead of `X | None` for compatibility
- Use `list[X]`, `dict[X, Y]` instead of `List`, `Dict` (Python 3.9+)

```python
# Good
def get_user(user_id: int) -> Optional[User]:
    ...

# Avoid
def get_user(user_id):  # No type hints
    ...
```

### Pydantic Models

- Use Pydantic `BaseModel` for data validation
- Always inherit from `BaseModel` for request/response models
- Use Pydantic v2 (not v1)

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
```

### Error Handling

- Use appropriate exception types
- Let FastAPI handle HTTP exceptions naturally
- Use `try/except` only when you can meaningfully handle the error
- Avoid catching generic `Exception` or `BaseException`

### FastAPI Best Practices

- Use Pydantic models for request/response bodies
- Define enums for fixed sets of values
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)

### Testing

- Place tests in `tests/` directory
- Test file naming: `test_<module>.py`
- Test function naming: `test_<description>`

---

## File Structure

```
payroll_manager/
├── main.py              # Application entry point
├── tests/
│   └── test_app.py      # Tests
├── pyproject.toml       # Project config (ruff)
├── pyrightconfig.json   # Type checking config
├── requirements.txt     # Dependencies
└── .pre-commit-config.yaml
```

---

## Common Issues

1. **ImportError: No module named 'app'**: The app is in `main.py`, not an `app/` directory. Use `from main import app`.

2. **Pydantic Error**: Ensure models inherit from `BaseModel` (Pydantic v2), not plain Python classes.

3. **Type Errors**: Run `pyright` to check for strict type errors.

4. **Lint Errors**: Run `ruff check .` to identify and fix linting issues.
