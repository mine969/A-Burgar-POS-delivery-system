# How to Write the Backend (Logic Guide)

**Goal**: This guide teaches you how to *think* like a backend developer so you can write this code yourself.

---

## 1. Starting from Scratch (`main.py`)

**The Logic**: Every program needs a starting point. In Python web apps, we call this the "App Instance".

**How to think about it**:
Imagine you are opening a restaurant.
1.  **Create the Building**: `app = FastAPI()`
    *   *Why?*: This creates the empty shell of your application.
2.  **Open the Doors (CORS)**: `app.add_middleware(...)`
    *   *Why?*: By default, browsers are paranoid. They won't let a website on port 3000 talk to a server on port 8000. You have to explicitly say "It's okay, I know this guy."
3.  **Hire Departments (Routers)**: `app.include_router(...)`
    *   *Why?*: You don't want one person doing everything. You split work into "Auth", "Orders", "Menu". You write them in separate files and then "hire" (include) them here.

---

## 2. Protecting the App (`auth.py`)

**The Logic**: We need a way to know *who* is talking to us without asking for their password every single time.

**How to think about it**:
1.  **The Login**: User gives `email` + `password`.
2.  **The Check**: You look up the email in the DB. If the password matches (after un-hashing it), they are good.
3.  **The Wristband (JWT)**: Instead of keeping them logged in on the server (which takes up memory), you give them a digital wristband (Token).
    *   *Write this logic*: "Take their email, add an expiration date (e.g., 30 mins), and sign it with my secret pen (SECRET_KEY)."
4.  **The Bouncer (`get_current_user`)**:
    *   *Write this logic*: "For every request to a protected page, check if they have a wristband. If the signature is valid, let them in. If not, kick them out."

---

## 3. Handling Orders (`routers/orders.py`)

**The Logic**: This is where the actual work happens.

**How to think about it**:
1.  **The Input**: A user sends data (e.g., "I want a burger").
    *   *Code*: `order: OrderCreate` (This ensures they actually sent valid data).
2.  **The Context**: Who is asking?
    *   *Code*: `current_user = Depends(get_current_user)` (The Bouncer tells you who this is).
3.  **The Action**:
    *   Create a new row in the `orders` table.
    *   Link it to the `current_user.id`.
    *   Save it to the database.
4.  **The Response**: Send back a receipt (e.g., "Order #123 created").

---

## 4. Your Turn: How to Rewrite It
1.  Create `main.py`. Just try to get a "Hello World" on the screen.
2.  Create `models/user.py`. Define what a "User" looks like in the database.
3.  Create `routers/users.py`. Write a function to save a user to the DB.
4.  Connect them in `main.py`.
