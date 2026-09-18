# Deployment Notes

## MVP
- Frontend can be hosted on any static Node/Vite-compatible platform.
- FastAPI can run behind a reverse proxy.
- PostgreSQL/PostGIS should be managed with automated backups.
- Redis is optional until asynchronous ingestion is enabled.

## Production hardening
- Replace public demo routing/geocoding with infrastructure appropriate to expected traffic.
- Add authentication for private ingestion/admin endpoints.
- Restrict CORS to deployed origins.
- Add rate limiting, request IDs, structured logs and monitoring.
- Pin tile and data-provider terms/attribution.
- Add circuit breakers and stale-data indicators.
- Encrypt secrets through a secret manager; never ship keys to the frontend.
- Add automated geospatial data validation.
- Validate route-risk models against historical events before any operational claim.
