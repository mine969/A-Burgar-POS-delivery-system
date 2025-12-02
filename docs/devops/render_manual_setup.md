# Manual Render Deployment Guide

This guide walks you through deploying the application on Render **without** using the Blueprint feature.

## Step 1: Create PostgreSQL Database

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **PostgreSQL**
3. Configure:
   - **Name**: `food-delivery-db`
   - **Database**: `food_delivery`
   - **User**: `food_delivery_user`
   - **Region**: Choose closest to you (e.g., Singapore)
   - **Plan**: **Free**
4. Click **Create Database**
5. Wait for it to provision (takes ~1 minute)
6. **Copy the Internal Database URL** (you'll need this in Step 2)
   - Go to the database page → **Info** section → Copy **Internal Database URL**

## Step 2: Create Web Service

1. Click **New +** → **Web Service**
2. Connect your GitHub repository
3. Configure the service:

### Basic Settings

- **Name**: `food-delivery-api`
- **Region**: Same as your database (e.g., Singapore)
- **Branch**: `main` (or your default branch)
- **Root Directory**: `backend`
- **Environment**: **Docker**
- **Dockerfile Path**: `Dockerfile`

### Instance Type

- **Plan**: **Free**

### Environment Variables

Click **Add Environment Variable** for each:

| Key            | Value                                           |
| -------------- | ----------------------------------------------- |
| `DATABASE_URL` | Paste the **Internal Database URL** from Step 1 |
| `PORT`         | `8000`                                          |

### Start Command

**IMPORTANT**: Override the default start command with:

```bash
sh -c 'python app/seed_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000'
```

This command:

1. Runs `seed_db.py` to initialize the database
2. Starts the FastAPI server with uvicorn

### Build Command

Leave as default (Docker build)

4. Click **Create Web Service**

## Step 3: Monitor Deployment

1. Watch the deployment logs
2. Look for:
   - "Creating tables..."
   - "Seeding Users..."
   - "Data seeded successfully!"
   - "Uvicorn running on..."

## Step 4: Test Your API

Once deployed, your API will be at: `https://food-delivery-api.onrender.com`

Test it:

- `https://food-delivery-api.onrender.com/docs` - API documentation
- `https://food-delivery-api.onrender.com/api/menu` - Menu items

## Troubleshooting

### "gunicorn: command not found"

- **Cause**: Render is using the wrong start command
- **Fix**: Update the **Start Command** in service settings to the one above

### "No module named 'app'"

- **Cause**: Root Directory is not set correctly
- **Fix**: Ensure **Root Directory** is set to `backend`

### Database connection errors

- **Cause**: DATABASE_URL is incorrect or database isn't ready
- **Fix**:
  1. Verify the DATABASE_URL in environment variables
  2. Ensure the database status is "Available"
  3. Use the **Internal Database URL**, not the external one

### Seed script runs every time

- This is expected on the free tier (container restarts frequently)
- The script checks if data exists before seeding
- No duplicate data will be created
