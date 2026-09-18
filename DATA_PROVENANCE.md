# Data Provenance Policy

PATHSAFE must never present a source as connected unless an adapter successfully fetches it.

For every dataset record:
- Provider
- Dataset/type
- Coverage
- Last successful update timestamp
- License/terms
- Ingestion status
- Confidence / quality metadata

The MVP has live Open-Meteo weather plus OSM-derived routing/geocoding adapters. Tamil Nadu government, Sentinel/NASA and DEM sources are adapter-ready but are not falsely represented as live integrations. Before enabling a source in production, verify its current API/data access, terms, rate limits, attribution requirements and update cadence.
