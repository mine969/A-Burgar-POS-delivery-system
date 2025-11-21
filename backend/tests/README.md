# Test Suite for Food Delivery Backend

This directory contains automated tests for the backend API.

## Running Tests

### Run all tests:

```bash
cd backend
pytest
```

### Run with verbose output:

```bash
pytest -v
```

### Run specific test file:

```bash
pytest tests/test_users.py
```

### Run with coverage report:

```bash
pytest --cov=app --cov-report=html
```

## Test Structure

- `conftest.py` - Test configuration and fixtures
- `test_auth.py` - Authentication tests
- `test_users.py` - User management tests
- `test_orders.py` - Order functionality tests (to be added)
- `test_menu.py` - Menu management tests (to be added)

## Test Database

Tests use an in-memory SQLite database that is created fresh for each test, ensuring test isolation.
