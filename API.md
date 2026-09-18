# API Reference

## GET /api/weather
Query: `lat`, `lon`

Returns the upstream Open-Meteo response.

## GET /api/hazards
Query: `lat`, `lon`, `demo`

Returns connected hazard layers. Demo returns explicitly simulated Chennai flood geometry.

## GET /api/facilities
Query: `lat`, `lon`, `demo`

Facility adapter placeholder. No capacity is fabricated.

## POST /api/routes/analyze
```json
{"origin":{"lat":13.08,"lon":80.27},"destination":{"lat":13.07,"lon":80.26},"mode":"normal","demo":true}
```

Returns route alternatives with distance, time, estimated risk, risk level, confidence, factors and GeoJSON geometry.

## POST /api/risk/predict
Reserved for trained research models.

## GET /api/sources
Returns the source registry.

## GET /api/system/status
Returns component health and model status.
