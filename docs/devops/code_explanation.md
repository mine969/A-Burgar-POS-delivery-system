# How to Ship Code (DevOps Logic Guide)

**Goal**: Understand the journey of code from your laptop to the server.

---

## 1. The Lunchbox (`Dockerfile`)

**The Logic**: "It works on my machine" is the biggest lie in programming. We need it to work *everywhere*.

**How to think about it**:
Imagine you are sending your kid to school with lunch.
-   If you just give them ingredients (raw code), they can't eat.
-   You need to pack a lunchbox (Container) with everything prepared.

**Writing the Code**:
1.  **The Box**: `FROM python:3.11` (Start with a box that has Python).
2.  **The Utensils**: `COPY requirements.txt` (What tools do we need?).
3.  **The Prep**: `RUN pip install ...` (Get the tools ready).
4.  **The Food**: `COPY . .` (Put the actual code in).
5.  **Eat**: `CMD ["uvicorn" ...]` (How to start the app).

---

## 2. The Team Manager (`docker-compose.yml`)

**The Logic**: Your app isn't just one thing. It's a Backend, a Frontend, and a Database. They need to talk to each other.

**How to think about it**:
-   You are the conductor of an orchestra.
-   **Service 1 (DB)**: "You sit here. Start first."
-   **Service 2 (Backend)**: "You sit next to DB. Don't play a note until DB is ready." (`depends_on`)
-   **Networking**: "I will put you all in the same room so you can hear each other." (Docker automatically does this).

---

## 3. The Robot (`Jenkinsfile`)

**The Logic**: Doing this manually is boring and error-prone. Let's build a robot to do it.

**How to think about it**:
1.  **The Trigger**: "Robot, watch this Git folder. If anything changes..." (`pollSCM`)
2.  **Step 1**: "Build the lunchboxes." (`docker-compose build`)
3.  **Step 2**: "Ship them to the server and open them." (`docker-compose up -d`)

---

## 4. Your Turn: How to Rewrite It
1.  **Docker**: Try to run your Python app in a container locally. Write a `Dockerfile` until `docker build` works.
2.  **Compose**: Try to run Python + MySQL together. Write `docker-compose.yml` until they can talk.
3.  **Jenkins**: Write a simple pipeline that just says "Hello" first. Then add the build commands.
