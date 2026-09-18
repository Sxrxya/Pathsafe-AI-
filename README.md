# PATHSAFE AI

**Find the safer way out.**

AI-powered routing for uncertain disaster conditions.

PATHSAFE AI is a research-oriented emergency routing MVP. It combines route geometry with weather, terrain, hazard and data-confidence signals. It does **not** guarantee safety and is not an official emergency service.

## Features
- Map-first React + TypeScript UI using MapLibre GL JS
- Demo Mode: Chennai flood scenario with simulated hazards, route alternatives and uncertainty
- Live weather adapter using Open-Meteo
- Route adapter using OSRM-compatible public routing service
- Geocoding through Nominatim adapter
- FastAPI backend with clean provider/service boundaries
- Risk model separated from routing and data ingestion so research models can replace it later
- Explainable route factors and first-class confidence/uncertainty
- Emergency Mode and responsive mobile navigation
- Data provenance/source registry
- Docker Compose for PostgreSQL/PostGIS + Redis + API + frontend

## Quick start

### 1. Local development
```bash
# backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# frontend, in another terminal
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

### 2. Docker
```bash
docker compose up --build
```
Frontend: http://localhost:5173
API: http://localhost:8000/docs

## Environment
Copy `.env.example` to `.env`. No frontend secrets are required.

The public services used by default are replaceable. For a real deployment, configure your own hosted routing, geocoding and tile infrastructure according to each provider's terms, rate limits and attribution requirements.

## Safety
PATHSAFE AI provides decision-support information, not guaranteed safety. Conditions can change rapidly during disasters. Always follow official emergency instructions and local authorities.

The demo scenario is explicitly simulated and must never be presented as live emergency information.

## Architecture
```text
React / MapLibre
      |
      v
FastAPI API
  |   |   |\
  |   |   | \--> Source registry / provenance
  |   |   \----> Risk + uncertainty model
  |   \--------> Weather adapter
  \------------> Routing + geocoding adapters
      |
 PostgreSQL + PostGIS / Redis

Future research path:
Sentinel/SAR + optical + DEM + weather + roads + government data
              -> feature extraction
              -> multimodal model
              -> hazard projection
              -> graph route risk
              -> uncertainty calibration
```

## API
- `GET /api/weather?lat=...&lon=...`
- `GET /api/hazards?lat=...&lon=...&demo=true`
- `GET /api/facilities?lat=...&lon=...&demo=true`
- `POST /api/routes/analyze`
- `POST /api/risk/predict`
- `GET /api/sources`
- `GET /api/system/status`

## Research limitations
The initial route risk formula is a transparent prototype, not a validated scientific model. A future release should be evaluated with historical flood maps, road closures, route travel-time observations, calibration metrics and out-of-distribution tests. Avoid interpreting demo risk percentages as operational probabilities.
