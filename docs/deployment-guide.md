# Backend Deployment Guide

**Author:** Lydiah (DevOps)  
**Last Updated:** February 17, 2026  
**Platform:** Render (Free Tier)

---

## Overview

This guide documents how the SolarSense backend is deployed to Render. It covers the full process from setting up the database to deploying the Node.js application.

The backend code lives in the **Backend repository** (`SolarSense-Capstone/Backend`). DevOps takes that code and deploys it — we do not write or change backend code.

---

## Prerequisites

Before deploying, you need:

- Access to the GitHub organisation: `SolarSense-Capstone`
- A Render account (sign up at render.com using GitHub login)
- The backend repo pushed to the `main` branch and working
- The list of environment variables from the Backend team

---

## Part 1: Create the PostgreSQL Database

Do this first. The backend needs a database URL before it can start.

**In the Render Dashboard:**

1. Click **New +** → **PostgreSQL**
2. Fill in the form:
   ```
   Name:     solarsense-db
   Database: solarsense_db
   User:     solarsense_admin
   Region:   Oregon (US West)
   Plan:     Free
   ```
3. Click **Create Database**
4. Wait 2–3 minutes for provisioning
5. Once ready, click on the database
6. Scroll to **Connections**
7. Copy the **Internal Database URL** — it looks like:
   ```
   postgresql://solarsense_admin:xxxxxxx@dpg-xxxx.oregon-postgres.render.com/solarsense_db
   ```
8. Save this somewhere safe — you will paste it as `DATABASE_URL` in the next step

> **Important:** Always use the **Internal** Database URL (not External) when both the database and web service are on Render. Internal URLs are faster and free.

---

## Part 2: Create the Web Service

1. Click **New +** → **Web Service**
2. Connect the Backend GitHub repository:
   - Click **Connect GitHub**
   - Select: `SolarSense-Capstone/Backend`
   - Click **Connect**
3. Configure the service:
   ```
   Name:          solarsense-backend
   Region:        Oregon (US West)   ← must match database region
   Branch:        main
   Runtime:       Node
   Build Command: npm install && npx prisma generate && npx prisma migrate deploy
   Start Command: npm start
   ```
4. **Do not click Create yet** — scroll down to add environment variables first

---

## Part 3: Add Environment Variables

Still on the same page, scroll to **Environment Variables** and add each one:

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | postgresql://... | Paste Internal Database URL from Part 1 |
| `DSE_BASE_URL` | https://dse-models-production.up.railway.app/api/v1 | DSE team's Railway URL |
| `API_KEY` | QfBmvo3htYQPSJWYYLcChxXvZonTuC2U | DSE API key |
| `PORT` | 3000 | Port the app runs on |
| `USER_AGENT` | SolarSense-Backend/1.0 | Required for Nominatim geocoding |
| `NODE_ENV` | production | Tells app it's in production |

After adding all 6 variables, click **Create Web Service**.

---

## Part 4: Watch the Deployment Logs

Render will start building immediately. Watch for these lines in order:

```
==> Running build command...
added 167 packages          ← npm install worked
Prisma schema loaded        ← prisma generate worked
All migrations have been successfully applied  ← database tables created
==> Build successful ���
==> Deploying...
Database connected          ← app connected to postgres
Server running on port 3000 ← app is running
==> Your service is live ���
```

If you see **Database connected** and **Server running on port 3000**, the deployment succeeded.

---

## Part 5: Verify the Deployment

### Test 1: Browser health check
```
Open: https://solarsense-backend-zdrw.onrender.com/health
Expected: {"ok": true}
```

### Test 2: Main endpoint (Postman)
```
Method: POST
URL: https://solarsense-backend-zdrw.onrender.com/api/v1/analyze

Headers:
  Content-Type: application/json

Body:
{
  "businessType": "Cafe",
  "country": "Kenya",
  "city": "Nairobi",
  "currency": "USD",
  "equipment": [
    {
      "type": "refrigerator",
      "quantity": 2,
      "hoursPerDay": 24
    }
  ],
  "tariff": 0.15,
  "uses_diesel": false
}

Expected: JSON response with viability_score, status, monthly_savings
```

If both tests return the expected responses, the deployment is complete.

---

## Part 6: Notify the Team

Post in the Teams channel with:
- Production URL
- Health endpoint confirmation
- Tag Sarah (Backend), Tianaah (Frontend), Security team

---

## About the Build Command

```bash
npm install && npx prisma generate && npx prisma migrate deploy
```

This runs three things in sequence:

1. `npm install` — installs all Node.js dependencies
2. `npx prisma generate` — generates the Prisma client from the schema
3. `npx prisma migrate deploy` — creates/updates database tables

Running migrations in the build command means they run automatically on every deployment. This is safe — Prisma skips migrations that have already been applied.

---

## What the Migrations Create

The build command applied 2 migrations:

```
20260208150341_init              ← initial schema
20260213143634_aligned_models    ← schema updates
```

These created 3 database tables:
- `Assessment` — stores business info and location
- `EquipmentItem` — stores equipment list per assessment
- `AssessmentResult` — stores viability results and model outputs

---

## Deployment Checklist

Use this before every deployment:

```
PRE-DEPLOYMENT:
[ ] Backend code is pushed to main branch
[ ] requirements/dependencies are up to date
[ ] Environment variables list received from Backend team
[ ] Database is created and running in Render

DEPLOYMENT:
[ ] Build command includes prisma generate and migrate deploy
[ ] All 6 environment variables added
[ ] Region matches between database and web service
[ ] Service created and deploying

POST-DEPLOYMENT:
[ ] Logs show "Database connected"
[ ] Logs show "Server running on port 3000"
[ ] Health endpoint returns {"ok": true}
[ ] Postman test returns viability score
[ ] Production URL shared with team
[ ] UptimeRobot monitoring confirmed active
```

---

## Common Errors and Fixes

### "Cannot GET /"
Not an error. The backend has no root route. Use `/health` instead.

### "relation does not exist" or table errors
Migrations did not run. Update build command to include:
```
npx prisma generate && npx prisma migrate deploy
```
Then redeploy.

### "Database connected" missing from logs
Check `DATABASE_URL` environment variable. Must be the Internal URL from Render PostgreSQL, not the External URL.

### Build fails with "Cannot find module"
A dependency is missing from `package.json`. Report to Sarah (Backend team).

### App starts but returns 500 errors
This is a code issue, not a deployment issue. Share the Render logs with Sarah.

---

## Redeployment

Render automatically redeploys when new code is pushed to the `main` branch.

To trigger a manual redeploy:
1. Go to the web service in Render Dashboard
2. Click **Manual Deploy**
3. Select **Deploy latest commit**

---

## Accessing Logs

1. Render Dashboard → `solarsense-backend`
2. Click **Logs** tab
3. Click **Live tail** to watch in real time

Useful for debugging during integration testing or if the team reports issues.
