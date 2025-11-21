# Backend Technical Documentation

## Technology Stack
-   **Framework**: FastAPI (Python 3.11)
-   **ORM**: SQLAlchemy
-   **Validation**: Pydantic
-   **Auth**: OAuth2 with JWT (JSON Web Tokens)

## Architecture
The backend follows a **Layered Architecture**:
1.  **Routers (`/routers`)**: Handle HTTP requests and responses.
2.  **Schemas (`/schemas`)**: Define data validation rules (Input/Output).
3.  **Models (`/models`)**: Define Database Tables.
4.  **Services/Utils**: `auth.py` for security, `database.py` for DB connection.

## API Specification
### Authentication (`/auth`)
-   `POST /login`: Accepts `username` (email) and `password`. Returns `access_token`.

### Users (`/users`)
-   `POST /`: Register a new user.
-   `GET /me`: Get current user details (Protected).

### Orders (`/orders`)
-   `POST /`: Create an order.
-   `GET /`: List orders.
    -   **Manager**: Returns all orders.
    -   **Driver**: Returns assigned orders.
    -   **Customer**: Returns own orders.

### Menu (`/menu`)
-   `GET /`: Public menu list.
-   `POST /`: Add item (Manager only).
