# SolarSense DevOps

**Owner:** Lydiah Nganga (DevOps Lead)  
**Project:** AI Solar Viability Assessment for Sub-Saharan African SMEs  
**Bootcamp:** DSE Capstone | February 2026

---

## Live Production

| Service | URL | Status |
|---------|-----|--------|
| Backend API | https://solarsense-backend-zdrw.onrender.com | ✅ Live |
| Health Check | https://solarsense-backend-zdrw.onrender.com/health | ✅ Live |

---

## What This Repo Contains

This repository documents deployment infrastructure, configurations, and operational procedures for the SolarSense platform.

> **Note:** Application code lives in the Backend and Frontend repositories.  
> This repo contains deployment documentation, monitoring setup, and operational guides.

---

## Repository Structure

```
Devops/
├── app/                        # Placeholder test app (FastAPI/Docker)
│   ├── main.py                 # Health check endpoints
│   └── requirements.txt        # Python dependencies
├── Dockerfile                  # Docker config for test app
├── docs/
│   ├── deployment-guide.md     # Step-by-step deployment instructions
│   ├── environment-variables.md # All required environment variables
│   ├── rollback-procedure.md   # How to rollback failed deployments
│   ├── monitoring-setup.md     # Monitoring and logging configuration
│   └── access-control.md       # Access control and security
└── README.md                   # This file
```

---

## GitHub Organization Structure

**Organization:** SolarSense-Capstone

**Owners (2):**
- Lydiah Nganga (DevOps)
- Tessa (DSE/Technical Lead)

**Repositories (6):**
1. **Frontend** - React application (Vercel/Netlify)
2. **Backend** - Node.js/Express API (Render)
3. **DSE-models** - Machine learning models (Railway)
4. **Devops** - Deployment documentation (this repo)
5. **Cybersecurity** - Security documentation and procedures
6. **Product-Design** - Design assets and documentation

**Access Model:**
- Maintain access: Team members have full access to their own repo
- Read access: All teams can view other repos
- Admin access: Owners (Lydiah & Tessa) have admin rights across all repos

---

## Platform Overview

| Component | Platform | Managed By |
|-----------|----------|------------|
| Backend Hosting | Render (Web Service) | DevOps |
| Database | Render (PostgreSQL) | DevOps |
| Monitoring | UptimeRobot | DevOps |
| Frontend Hosting | Vercel/Netlify | Frontend Team |
| DSE Models | Railway | DSE Team |

---

## Tech Stack

### Backend (Deployed by DevOps)
- **Runtime:** Node.js 22
- **Framework:** Express
- **ORM:** Prisma
- **Database:** PostgreSQL
- **External APIs:** 
  - NASA POWER (solar irradiance data)
  - Nominatim (geocoding)
  - DSE Models API (ML predictions)

### Infrastructure
- **Hosting:** Render (Free Tier)
- **Database:** Render PostgreSQL (Free Tier)
- **Monitoring:** UptimeRobot (Free Tier)
- **SSL/TLS:** Render managed certificates

---

## API Endpoints (Backend)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check → `{"ok": true}` |
| POST | /api/v1/analyze | Main solar viability assessment |
| POST | /api/v1/assessments | Create assessment with database storage |
| GET | /api/v1/assessments/:id | Retrieve assessment by ID |
| GET | /api/v1/assessments/:id/report | Download PDF report |

---

## Quick Reference

### Deploy Backend
See: `docs/deployment-guide.md`

**Build Command:**
```bash
npm install && npx prisma generate && npx prisma migrate deploy
```

**Start Command:**
```bash
npm start
```

### Environment Variables
See: `docs/environment-variables.md`

Required variables:
- `DATABASE_URL` - PostgreSQL connection string (Render)
- `DSE_BASE_URL` - DSE models API base URL (Railway)
- `API_KEY` - DSE models authentication key
- `PORT` - Application port (3000)
- `USER_AGENT` - Nominatim geocoding identifier
- `NODE_ENV` - Environment (production)

### Rollback Procedure
See: `docs/rollback-procedure.md`

If deployment fails:
1. Go to Render Dashboard → Events tab
2. Find last successful deployment
3. Click "Rollback to this deploy"
4. Wait 2-3 minutes for rollback completion
5. Verify health endpoint works

### Monitoring
See: `docs/monitoring-setup.md`

- **Uptime:** UptimeRobot checks `/health` every 5 minutes
- **Logs:** Available in Render dashboard (7-day retention)
- **Alerts:** Email notifications for downtime

---

## Deployment History

| Date | Event | Details |
|------|-------|---------|
| Feb 9, 2026 | GitHub org created | 6 repositories, 2 owners |
| Feb 16, 2026 | Test app deployed | Validated Docker deployment pipeline |
| Feb 17, 2026 | Production backend deployed | Node.js backend live at Render |
| Feb 17, 2026 | Database configured | PostgreSQL with Prisma migrations |
| Feb 17, 2026 | Monitoring activated | UptimeRobot monitoring configured |
| Feb 17, 2026 | MFA enabled | Render account security hardened |
| Feb 17, 2026 | Frontend unblocked | Backend URL shared for integration |

---

## Test App (app/)

The `app/` folder contains a FastAPI Python application that was deployed early in the project to:

1. **Validate deployment pipeline** before the real backend was ready
2. **Learn Render configuration** in a low-risk environment
3. **Confirm GitHub-to-Render auto-deploy** worked correctly
4. **Test Docker containerization** with a simple app

This app is kept in the repo as:
- Evidence of the deployment validation process
- Reference for Docker configuration
- Backup test endpoint if needed

---

## Documentation

### For Deployment
- [Deployment Guide](docs/deployment-guide.md) - Complete deployment walkthrough
- [Environment Variables](docs/environment-variables.md) - All environment variables explained
- [Rollback Procedure](docs/rollback-procedure.md) - Emergency rollback steps

### For Operations
- [Monitoring Setup](docs/monitoring-setup.md) - How monitoring works
- [Access Control](docs/access-control.md) - Who has access to what

---

## Team Contacts

| Role | Name | Responsibility |
|------|------|----------------|
| DevOps Lead | Lydiah Nganga | Deployment, infrastructure, monitoring |
| Technical Lead | Tessa | Overall technical direction, DSE |
| Backend Lead | Sarah | Backend application code |
| Frontend Lead | Tianaah | Frontend application |
| Cybersecurity Lead | Lilly | Security review and compliance |

---

## Support During Demo Week

**Demo Dates:** February 25-27, 2026

**If backend issues during demo:**
1. Check UptimeRobot dashboard for service status
2. Review Render logs for errors
3. Contact Lydiah (DevOps) via Teams
4. Backup: Use pre-recorded demo video

**Emergency contacts available during demo week**

---

## Contributing

This is a bootcamp capstone project. The DevOps repo is maintained by Lydiah (DevOps Lead).

**For deployment issues:** Open an issue or contact in Teams  
**For backend code issues:** Refer to Backend repository  
**For frontend issues:** Refer to Frontend repository

---

## License

Bootcamp Capstone Project - SolarSense Team © 2026
