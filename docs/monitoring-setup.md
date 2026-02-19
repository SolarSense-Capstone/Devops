# Monitoring Setup

**Author:** Lydiah (DevOps)  
**Due Date:** February 19, 2026  


---

## Overview

This document describes how the SolarSense backend is monitored in production. For a free-tier MVP, we use lightweight tools that require no cost and minimal setup.

---

## UptimeRobot (Uptime Monitoring)

UptimeRobot pings the health endpoint every 5 minutes and sends an email alert if the service goes down.

**Setup steps:**
1. Go to https://uptimerobot.com
2. Sign up for a free account
3. Click **Add New Monitor**
4. Fill in:
   ```
   Monitor Type:    HTTP(s)
   Friendly Name:   SolarSense Backend
   URL:             https://solarsense-backend-zdrw.onrender.com/health
   Interval:        Every 5 minutes
   ```
5. Add alert email (your email)
6. Click **Create Monitor**

**What it checks:**
- Sends a GET request to `/health` every 5 minutes
- If response is not 200 OK → sends email alert
- Dashboard shows uptime percentage and response time history

<img width="1366" height="768" alt="uptime monitoring" src="https://github.com/user-attachments/assets/f589dc6b-4235-45d3-917c-ea0bd97e6e00" />


---

## Render Logs (Application Logging)

Render captures all console output from the backend automatically. No setup required.

**How to access:**
1. Render Dashboard → `solarsense-backend`
2. Click **Logs** tab
3. Click **Live tail** to watch in real time

**What to look for:**

Healthy logs look like:
```
Database connected
Server running on port 3000
GET /health 200
POST /api/v1/analyze 200
[COMPUTE] Assessment complete (DSE): { viability_score: 55.0 }
```

Warning signs:
```
[FALLBACK] Using backend fallback logic   ← DSE models unreachable
POST /api/v1/analyze 500                  ← Request failed
Error: connect ECONNREFUSED               ← Database or DSE unreachable
process.exit(1)                           ← App crashed
```

**When to check logs:**
- When frontend team reports errors
- After every new deployment
- During integration testing week
- Every morning during demo week (Feb 25–27)
  
<img width="1366" height="768" alt="render logs" src="https://github.com/user-attachments/assets/ed334203-6236-4dbd-93d4-89f8a651d144" />

---

## Daily Health Check Routine

During Week 2 (Feb 16–22) and demo week (Feb 23–27), run this quick check each morning:

```
1. Open UptimeRobot dashboard
   → Confirm: No downtime overnight

2. Open Render logs
   → Confirm: No red errors in last 24 hours

3. Open in browser:
   https://solarsense-backend-zdrw.onrender.com/health
   → Confirm: {"ok": true}

4. Post status in Teams:
   "☀️ Morning check: Backend healthy, uptime 100%, no errors"
```

---

## Render Free Tier Behaviour

The free tier has one important limitation: **services spin down after 15 minutes of inactivity.**

What this means:
- If no requests come in for 15+ minutes, the service goes to sleep
- The next request triggers a cold start (30–60 second delay)
- This is normal — not a crash or error

How UptimeRobot helps:
- Pinging every 5 minutes keeps the service warm during active periods
- During demo preparation, confirm monitoring is running

---

## What DevOps Does NOT Monitor

To be clear about scope:

| Thing | Who Monitors It |
|-------|----------------|
| Backend uptime | DevOps (UptimeRobot + Render logs) |
| API response correctness | Backend team (Sarah) |
| DSE model accuracy | DSE team |
| Frontend uptime | Frontend team (Vercel/Netlify dashboard) |
| DSE model uptime | DSE team (Railway dashboard) |
| Database performance | Render dashboard (automatic) |

---

## Escalation Process

If monitoring shows an issue:

1. Check Render logs for the error
2. Identify if it is infrastructure (DevOps) or code (Backend/DSE)
3. If infrastructure → fix it (see rollback-procedure.md)
4. If code → notify the relevant team with the error from logs
5. Post update in Teams channel within 15 minutes of detecting issue
