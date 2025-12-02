# Deploying Food Delivery App to Vercel

This guide outlines the steps to deploy your Food Delivery App (Frontend + Backend) to Vercel.

## Prerequisites

1.  **Vercel Account**: [Sign up here](https://vercel.com/signup).
2.  **GitHub Repository**: Ensure your code is pushed to GitHub.
3.  **Database**: You need a cloud database. Vercel Postgres is recommended for ease of use, or you can use Neon, Supabase, or PlanetScale.

---

## Part 1: Database Setup (Vercel Postgres)

1.  Go to your Vercel Dashboard.
2.  Click **Storage** -> **Create Database** -> **Postgres**.
3.  Give it a name (e.g., `food-delivery-db`) and create it.
4.  Once created, go to the **.env.local** tab (or "Quickstart") and copy the connection details.
    - You specifically need the `POSTGRES_URL` or `DATABASE_URL`.
    - _Note_: If using Vercel Postgres, the URL usually starts with `postgres://`. SQLAlchemy supports this.

---

## Part 2: Deploy Backend

We will deploy the backend as a separate Vercel project.

1.  **Import Project**:
    - Go to Vercel Dashboard -> **Add New...** -> **Project**.
    - Select your GitHub repository (`A-Burgar-POS-delivery-system`).
2.  **Configure Project**:
    - **Project Name**: `food-delivery-backend` (or similar).
    - **Root Directory**: Click "Edit" and select `backend`.
    - **Framework Preset**: Vercel should detect "Other" or "Python". If not, leave as default.
3.  **Environment Variables**:
    - Add `DATABASE_URL` and paste your database connection string from Part 1.
    - Add `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` if you prefer individual vars, but `DATABASE_URL` is sufficient if your code uses it (which it does).
    - _Important_: If using Vercel Postgres, the variable is often `POSTGRES_URL`. You might need to alias it to `DATABASE_URL` in the Vercel UI or update your code to check `POSTGRES_URL`.
4.  **Deploy**: Click **Deploy**.
5.  **Result**: Once deployed, you will get a URL (e.g., `https://food-delivery-backend.vercel.app`). **Copy this URL.**

---

## Part 3: Deploy Frontend

Now we deploy the Next.js frontend.

1.  **Import Project**:
    - Go to Vercel Dashboard -> **Add New...** -> **Project**.
    - Select the **same** GitHub repository again.
2.  **Configure Project**:
    - **Project Name**: `food-delivery-frontend`.
    - **Root Directory**: Click "Edit" and select `frontend-demo`.
    - **Framework Preset**: Vercel should automatically detect **Next.js**.
3.  **Environment Variables**:
    - Add `NEXT_PUBLIC_API_URL`.
    - Value: The URL of your backend from Part 2 (e.g., `https://food-delivery-backend.vercel.app`).
    - _Note_: Do not add a trailing slash.
4.  **Deploy**: Click **Deploy**.

---

## Part 4: Final Configuration

1.  **CORS**:
    - Your backend currently allows `localhost`. You might need to update `backend/app/main.py` to allow your new frontend domain (e.g., `https://food-delivery-frontend.vercel.app`).
    - _Quick Fix_: Add `"*"` to `origins` in `backend/app/main.py` or add the specific Vercel domain.
2.  **Database Initialization**:
    - The tables need to be created.
    - Your backend code has `Base.metadata.create_all(bind=engine)` in `main.py`, so tables should be created automatically when the backend starts.
    - **Seeding**: You might need to run a script to seed the initial data (menu items, admin user). You can run this locally by connecting to the remote DB, or create a temporary API endpoint to seed data.

## Important Notes

- **File Uploads**: Vercel Serverless Functions are ephemeral and **cannot store files** locally in `static/`.
  - Your current setup saves images to `static/`. This **will not work** on Vercel for uploaded files.
  - You must switch to a cloud storage provider like **AWS S3**, **Vercel Blob**, or **Cloudinary** for image uploads.
  - Images already in the repo (committed code) will be served fine, but new uploads will fail or disappear.
