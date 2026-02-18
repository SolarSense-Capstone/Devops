# Rollback Procedure

**Author:** Lydiah (DevOps)  
**Due Date:** February 19, 2026  
**Last Updated:** February 17, 2026

---

## Overview

This document explains what to do if a deployment fails or the production backend breaks. The goal is to restore service as quickly as possible, especially during the demo period (February 25–27).

---

## Step 1: Identify the Problem

Before doing anything, check the Render logs to understand what went wrong.

**How to access logs:**
1. Go to Render Dashboard
2. Click `solarsense-backend`
3. Click the **Logs** tab
4. Read the error messages

**Common error patterns:**

| Error in Logs | What It Means |
|---------------|---------------|
| `Cannot find module` | Missing npm dependency |
| `relation does not exist` | Database migration did not run |
| `ECONNREFUSED` | Cannot connect to database |
| `Prisma Client is not configured` | `prisma generate` did not run |
| `Port already in use` | App crashed and restarted on wrong port |
| `process.exit(1)` | App failed to start, check lines above |

---

## Step 2: Quick Fixes (Try These First)

### Fix 1: Wrong Environment Variable
If logs show a connection error or missing config:
1. Go to Render Dashboard → `solarsense-backend` → **Environment** tab
2. Check all 6 variables are present and correct
3. Click **Save Changes** (triggers automatic redeploy)
4. Watch logs — should fix in 2–3 minutes

### Fix 2: Build Command Issue
If logs show Prisma errors:
1. Go to **Settings** tab → **Build Command**
2. Confirm it reads exactly:
   ```
   npm install && npx prisma generate && npx prisma migrate deploy
   ```
3. Save → Manual Deploy → Deploy latest commit

### Fix 3: Code Bug (Backend Team Issue)
If logs show an application error after startup:
1. This is NOT a deployment issue — it is a code bug
2. Copy the error from logs
3. Send to Sarah (Backend) immediately
4. Do not try to fix code yourself

---

## Step 3: Rollback to a Previous Deployment

If the latest deployment broke something that was working before, roll back to the previous version.

**In Render Dashboard:**
1. Click `solarsense-backend`
2. Click the **Events** tab
3. Find the last deployment that was working (look for green "Deploy succeeded")
4. Click **Rollback to this deploy**
5. Confirm the rollback
6. Watch logs — should restore in 2–3 minutes
7. Test health endpoint: `https://solarsense-backend-zdrw.onrender.com/health`

> **Note:** Rolling back does NOT undo database migrations. If a migration was applied, it stays. Only the application code is rolled back. If this causes issues, contact Sarah immediately.

---

## Step 4: Nuclear Option (Full Redeploy from Scratch)

Only do this if rollback does not work and the service is completely broken.

**Save first:**
1. Go to **Environment** tab
2. Write down all 6 environment variables and their values somewhere safe
3. You will need to re-enter them

**Delete and recreate:**
1. In Render Dashboard → `solarsense-backend` → **Settings**
2. Scroll to the bottom → **Delete Web Service**
3. Confirm deletion
4. Follow the full deployment guide from scratch: `docs/deployment-guide.md`
5. Re-enter all environment variables

> **Warning:** Only do this as a last resort. It takes 10–15 minutes.

---

## Step 5: Notify the Team

Whenever there is a deployment issue, post in the Teams channel immediately:

```
��� DEPLOYMENT ISSUE

Service: solarsense-backend
Status: [Down / Degraded / Investigating]
Started: [time]
Impact: [Frontend cannot connect / API returning errors / etc.]

What I'm doing: [checking logs / rolling back / fixing env var]
ETA: [5 min / 15 min / unknown]

@Tessa @Sarah - heads up
```

And when resolved:
```
✅ DEPLOYMENT RESTORED

Service: solarsense-backend
Status: Live
Fix applied: [what you did]
Downtime: [how long it was down]

Health check confirmed: https://solarsense-backend-zdrw.onrender.com/health
```

---

## Demo Day Emergency Plan (February 25–27)

The demo is critical. If the service goes down during the demo:

**Immediate actions (first 2 minutes):**
1. Check UptimeRobot alert — confirm service is actually down
2. Open Render logs — identify error
3. Attempt Quick Fix 1 (environment variable check)
4. If not fixed in 2 minutes → move to backup plan

**Backup plan:**
- If team recorded a demo video beforehand, switch to video
- Presenter continues talking while DevOps works on fix
- Do not panic in front of the audience

**Emergency contacts during demo:**
- Tessa (TL): [contact in Teams]
- Sarah (Backend): [contact in Teams]
- Mentor: [contact in Teams]

---

## Render Free Tier Note

On the free tier, Render web services spin down after 15 minutes of inactivity. When a request comes in after spin-down, the service takes **30–60 seconds to restart**. This is not a crash — it is normal behaviour.

To reduce this during demo week:
- UptimeRobot pings the health endpoint every 5 minutes, which keeps the service warm
- Confirm UptimeRobot is active before the demo

---

## Checklist Before Demo Day (February 24)

```
[ ] Service is live and responding
[ ] Health endpoint returns {"ok": true}
[ ] UptimeRobot monitoring is active
[ ] All environment variables confirmed in Render
[ ] Rollback option tested (at least one previous deploy in Events tab)
[ ] Emergency contacts saved and reachable
[ ] Backup demo video recorded (owned by PM team)
```
