# PATHSAFE AI Architecture

## Product loop
`MAP → HAZARDS → ROUTES → RISK → CONFIDENCE → DECISION`

## Layers
1. **Provider adapters** isolate external APIs and make sources replaceable.
2. **Ingestion** should normalize weather, road, DEM, satellite and government observations into a common geospatial model.
3. **Feature extraction** produces road-segment features: precipitation, elevation, slope, flood exposure, blockage evidence and source freshness.
4. **Risk model** estimates relative route risk. The MVP uses a transparent heuristic; production research should use trained and validated models.
5. **Uncertainty** is computed separately from risk and should account for missing modalities, stale observations and model calibration.
6. **Decision support UI** presents alternatives without claiming a route is guaranteed safe.

## Suggested PostGIS schema
See `docs/DATA_MODEL.sql`.

## Research roadmap
- Historical flood labels from authoritative/public datasets
- Sentinel-1 SAR flood segmentation
- DEM-derived elevation/slope features
- Graph neural network or learned edge-risk model
- Calibration and conformal/ensemble uncertainty
- Missing-modality experiments
- OOD evaluation by storm, geography and season
