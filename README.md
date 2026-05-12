# sample-notification-service

A sample notification microservice used to test the tech-stack-advisor
multi-repo analysis.

## Dependencies on other sample repos

- `sample-legacy-app` (npm) — calls its `/api/events` endpoint
- Inter-repo dependency intentionally outdated

## What this exercises in the analyzer

- **Shared deps** with `sample-legacy-app` and `sample-dashboard-app`:
  axios, lodash, express, requests, fastapi, pydantic
- **Version inconsistencies** — same packages pinned at different versions
- **Inter-repo dep** — `sample-legacy-app` listed as an npm dep
- **Outdated packages with CVEs** — nodemailer, ws, ioredis, jinja2, sqlalchemy

## Run locally

```
npm install
npm start

python -m celery -A worker.dispatcher worker
```
