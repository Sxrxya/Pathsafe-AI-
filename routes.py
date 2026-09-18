from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..services.providers import route_osrm, geocode, open_meteo
from ..services.risk import score_route

router=APIRouter()

SOURCES=[
 {"dataset":"OpenStreetMap","provider":"OpenStreetMap contributors","type":"Roads / POIs","coverage":"Global","status":"Connected","license":"ODbL"},
 {"dataset":"Open-Meteo","provider":"Open-Meteo","type":"Weather / precipitation","coverage":"Global","status":"Connected","license":"Provider terms apply"},
 {"dataset":"OSRM-compatible routing","provider":"Project OSRM public demo","type":"Road routing","coverage":"OSM coverage","status":"Connected","license":"OSRM / OSM terms apply"},
 {"dataset":"Nominatim","provider":"OpenStreetMap Foundation community service","type":"Geocoding","coverage":"Global","status":"Connected","license":"ODbL / usage policy applies"},
 {"dataset":"Tamil Nadu public datasets","provider":"Tamil Nadu government portals","type":"Government layers","coverage":"Tamil Nadu","status":"Adapter-ready; source availability varies","license":"Per source"},
 {"dataset":"Copernicus Sentinel / NASA / USGS","provider":"Public Earth observation providers","type":"Satellite / DEM","coverage":"Varies","status":"Adapter-ready; ingestion not enabled in MVP","license":"Per source"},
]

class Point(BaseModel): lat: float=Field(ge=-90,le=90); lon: float=Field(ge=-180,le=180)
class RouteRequest(BaseModel): origin: Point; destination: Point; mode: str="normal"; demo: bool=False

@router.get('/sources')
def sources(): return {"sources":SOURCES}

@router.get('/system/status')
def status(): return {"api":"ok","routing":"adapter-enabled","weather":"open-meteo-enabled","demo":True,"research_model":"heuristic-prototype"}

@router.get('/weather')
async def weather(lat:float,lon:float):
    return await open_meteo(lat,lon)

@router.get('/hazards')
def hazards(lat:float,lon:float,demo:bool=False):
    if demo:
        return {"mode":"simulation","hazards":[{"type":"flood","severity":"high","geometry":{"type":"Polygon","coordinates":[[[80.18,13.06],[80.25,13.06],[80.25,13.12],[80.18,13.12],[80.18,13.06]]]}}],"message":"SIMULATION — NOT LIVE EMERGENCY DATA"}
    return {"mode":"live","hazards":[],"message":"No connected hazard feed for this location in the MVP."}

@router.get('/facilities')
def facilities(lat:float,lon:float,demo:bool=False):
    return {"facilities":[],"message":"Facility discovery adapter is ready; connect Overpass or an official feed before operational use."}

@router.post('/routes/analyze')
async def analyze(req:RouteRequest):
    if req.demo:
        # Chennai demo geometries: clearly simulated and not navigation instructions.
        base=[[80.2707,13.0827],[80.2580,13.0710],[80.2450,13.0750],[80.2300,13.0900]]
        routes=[]
        for i,(name,km,minu,exp,missing) in enumerate([
            ("Safer Route",12.4,22,.18,False),("Faster but Riskier",9.8,18,.62,False),("Uncertain Route",11.2,20,.38,True)]):
            rr=score_route(km,{"rain":8,"precipitation":10,"wind_speed_10m":20},exp,missing,i)
            routes.append({"id":f"demo-{i+1}","name":name,"distance_km":km,"duration_min":minu,"risk":rr.score,"risk_level":rr.level,"confidence":rr.confidence,"factors":rr.factors,"geometry":{"type":"LineString","coordinates":[[80.2707,13.0827],[80.27-i*.01,13.075+i*.003],[80.245-i*.005,13.085+i*.004],[80.2300,13.0900]]}})
        return {"simulation":True,"routes":routes,"notice":"SIMULATION — NOT LIVE EMERGENCY DATA"}
    try:
        raw=await route_osrm(req.origin.model_dump(),req.destination.model_dump())
    except Exception as e: raise HTTPException(502,f"Routing provider unavailable: {e}")
    weather=await open_meteo(req.origin.lat,req.origin.lon)
    current=weather.get('current',{})
    routes=[]
    for i,r in enumerate(raw.get('routes',[])[:3]):
        rr=score_route(r['distance']/1000,current,0.25+i*.08,False,i)
        routes.append({"id":f"live-{i+1}","name":["Safer Route","Faster but Riskier","Uncertain Route"][min(i,2)],"distance_km":round(r['distance']/1000,1),"duration_min":round(r['duration']/60),"risk":rr.score,"risk_level":rr.level,"confidence":rr.confidence,"factors":rr.factors,"geometry":r['geometry']})
    return {"simulation":False,"routes":routes,"notice":"Risk estimates are prototype decision-support, not guarantees."}

@router.post('/risk/predict')
def predict(payload:dict):
    return {"model":"heuristic-prototype","status":"research-only","prediction":"Connect trained model here","uncertainty":"not calibrated"}
