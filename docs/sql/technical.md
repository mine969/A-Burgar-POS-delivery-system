# SQL Technical Documentation

## Technology
-   **Database Engine**: MySQL 8.0
-   **Driver**: `pymysql` (Python client)

## Schema Design
The database is normalized to 3NF (Third Normal Form) to reduce redundancy.

### Tables
1.  **`users`**:
    -   `id` (PK, Auto Increment)
    -   `email` (Unique Index)
    -   `hashed_password`
    -   `role` (Enum: manager, customer, driver, kitchen)

2.  **`orders`**:
    -   `id` (PK)
    -   `customer_id` (FK -> users.id)
    -   `status` (Index: PENDING, PREPARING, DELIVERING, COMPLETED)
    -   `total_price`

3.  **`driver_assignments`**:
    -   `order_id` (FK)
    -   `driver_id` (FK)
    -   `status` (Index: ACTIVE, COMPLETED)

## Performance
-   **Indexes**: Created on frequently filtered columns (`status`, `email`) to speed up `SELECT` queries.
