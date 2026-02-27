# Environment Variables

**Author:** Lydiah (DevOps)  
**Last Updated:** February 17, 2026

---

## Overview

All environment variables are configured in the Render dashboard under the web service's **Environment** tab. They are never stored in the GitHub repository.

The `.env` file is listed in `.gitignore` in the backend repo, which means it is never committed to GitHub. Variables are set manually in Render for production.

---

## Production Variables (Set in Render)

### DATABASE_URL
```
Key:   DATABASE_URL
Value: postgresql://solarsense_admin:xxxxx@dpg-xxxx.oregon-postgres.render.com/solarsense_db
```
- What it does: Connects the backend to the PostgreSQL database
- Where it comes from: Render generates this when you create a PostgreSQL service
- Always use the **Internal** URL (not External) when on Render
- Format: `postgresql://user:password@host:port/database`

---

### DSE_BASE_URL
```
Key:   DSE_BASE_URL
Value: https://dse-models-production.up.railway.app/api/v1
```
- What it does: Points the backend to the DSE ML models hosted on Railway
- Where it comes from: DSE team provided this URL
- The backend calls this to get solar viability predictions
- Owned and maintained by the DSE team (not DevOps)

---

### API_KEY
```
Key:   API_KEY
Value: QfBmvo3htYQPSJWYYLcChxXvZonTuC2U
```
- What it does: Authenticates the backend's requests to the DSE models
- Where it comes from: DSE team provided this key
- Sent as `X-API-KEY` header in DSE requests
- If this key is rotated, DSE team must provide a new one

---

### PORT
```
Key:   PORT
Value: 3000
```
- What it does: Tells the app which port to listen on
- Render routes external traffic to this port automatically
- Default in code is also 3000 (`process.env.PORT || 3000`)

---

### USER_AGENT
```
Key:   USER_AGENT
Value: SolarSense-Backend/1.0
```
- What it does: Identifies the app when making requests to Nominatim (geocoding)
- Nominatim (OpenStreetMap) requires a User-Agent header
- Without this, geocoding requests may be rate-limited or blocked

---

### NODE_ENV
```
Key:   NODE_ENV
Value: production
```
- What it does: Tells the app it is running in production mode
- Affects logging levels and error detail in responses
- Never set this to `development` in Render

---

## Variables NOT Needed

These were investigated but confirmed not required:

| Variable | Reason Not Needed |
|----------|------------------|
| NASA_API_KEY | NASA POWER API is free and public, no key required |
| GEOCODING_API_KEY | Using Nominatim (free, no key needed) |
| CORS_ORIGIN | Backend uses `cors({ origin: '*' })` — open for all origins |
| JWT_SECRET | No authentication implemented in MVP |

---

## How to Add or Update a Variable in Render

1. Go to Render Dashboard
2. Click on `solarsense-backend` web service
3. Click the **Environment** tab
4. Click **Add Environment Variable** or edit an existing one
5. Click **Save Changes**
6. Render will automatically redeploy with the new variable

---

## If a Variable Changes

| Scenario | Action |
|----------|--------|
| DATABASE_URL changes | Update in Render → save → redeploy |
| DSE_BASE_URL changes | DSE team notifies DevOps → update in Render |
| API_KEY rotated | DSE team provides new key → update in Render |
| New variable needed | Backend team notifies DevOps → add to Render |

---

## Security Notes

- Never share `API_KEY` or `DATABASE_URL` in public channels
- Use Teams DM or a secure channel to share secrets
- These values are stored securely by Render and are not visible in logs
- The `.gitignore` in the backend repo already excludes `.env`
