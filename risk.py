from dataclasses import dataclass

@dataclass
class RiskResult:
    score: float
    level: str
    confidence: str
    factors: list[str]

# Prototype heuristic only. Not a validated probability or safety guarantee.
def score_route(distance_km: float, weather: dict, hazard_exposure: float, data_missing: bool, index: int) -> RiskResult:
    rain=float(weather.get("rain",0) or 0); precip=float(weather.get("precipitation",0) or 0); wind=float(weather.get("wind_speed_10m",0) or 0)
    weather_risk=min(35, rain*5 + precip*3 + max(0,wind-25)*0.5)
    terrain_risk=min(25, 8 + index*3)
    flood_risk=min(35, hazard_exposure*35)
    road_risk=min(15, index*4)
    uncertainty=12 if data_missing else 3
    score=min(99, round(weather_risk+terrain_risk+flood_risk+road_risk+uncertainty,1))
    level="Low" if score<35 else "Medium" if score<65 else "High" if score<85 else "Unknown"
    confidence="Low" if data_missing else "Moderate" if score>60 else "High"
    factors=[]
    if rain>5 or precip>5: factors.append("Heavy rainfall nearby")
    if hazard_exposure>.45: factors.append("Flood exposure on route")
    if index>0: factors.append("Higher-risk road segments")
    if data_missing: factors.append("Recent satellite or blockage data unavailable")
    if not factors: factors.append("No major modeled hazard signal")
    return RiskResult(score,level,confidence,factors)
