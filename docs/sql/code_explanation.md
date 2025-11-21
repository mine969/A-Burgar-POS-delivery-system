# How to Design the Database (Logic Guide)

**Goal**: Understand *why* we structure data this way, so you can design your own database later.

---

## 1. The Foundation (`users` table)

**The Logic**: Everything starts with people.

**How to think about it**:
-   I need a list of people.
-   Each person needs a unique ID (like a Social Security Number) so I don't mix up two "John Smiths". -> `id INT AUTO_INCREMENT PRIMARY KEY`
-   I need to look them up by email fast. -> `UNIQUE INDEX`
-   I need to know if they are a Driver or a Customer. -> `role ENUM(...)`

**Writing the Code**:
```sql
CREATE TABLE users (
    id ...
    email ...
    role ...
);
```

---

## 2. The Connections (`orders` table)

**The Logic**: An order doesn't exist in a vacuum. It belongs to someone.

**How to think about it**:
-   I need a table for Orders.
-   **Crucial Step**: How do I link this order to John Smith?
    -   *Bad Way*: Write "John Smith" in the order row. (What if he changes his name?)
    -   *Good Way*: Write John's ID (`user_id = 5`).
-   **The Safety Net (Foreign Key)**:
    -   *Logic*: "Database, please promise me you will NEVER let me save an order for User ID 99 if User 99 doesn't exist."
    -   *Code*: `FOREIGN KEY (customer_id) REFERENCES users(id)`

---

## 3. The Performance (`INDEX`)

**The Logic**: As the app grows, finding things gets harder.

**How to think about it**:
-   Imagine a pile of 1,000,000 receipts on the floor.
-   Boss asks: "Give me all the PENDING orders."
-   Without an index, you pick up every single receipt to check. (Slow!)
-   With an index, you keep a separate clipboard list of just the "PENDING" ones.
-   *Code*: `CREATE INDEX idx_status ON orders(status);`

---

## 4. Your Turn: How to Rewrite It
1.  Start with paper. Draw boxes for "User", "Order", "Menu Item".
2.  Draw lines between them. "One User has Many Orders".
3.  Open `init.sql`.
4.  Write `CREATE TABLE` for the independent ones first (Users, Menu).
5.  Write `CREATE TABLE` for the dependent ones next (Orders link to Users).
