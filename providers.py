import os, httpx

ROUTING_URL = os.getenv("ROUTING_URL", "https://router.project-osrm.org")
GEOCODING_URL = os.getenv("GEOCODING_URL", "https://nominatim.openstreetmap.org")

async def route_osrm(origin, destination):
    url=f"{ROUTING_URL}/route/v1/driving/{origin['lon']},{origin['lat']};{destination['lon']},{destination['lat']}"
    params={"overview":"full","geometries":"geojson","alternatives":"true","steps":"false"}
    async with httpx.AsyncClient(timeout=15) as c:
        r=await c.get(url,params=params,headers={"User-Agent":"PATHSAFE-AI/0.1 research prototype"}); r.raise_for_status(); return r.json()

async def geocode(q):
    async with httpx.AsyncClient(timeout=10) as c:
        r=await c.get(f"{GEOCODING_URL}/search",params={"q":q,"format":"jsonv2","limit":5},headers={"User-Agent":"PATHSAFE-AI/0.1 research prototype"}); r.raise_for_status(); return r.json()

async def open_meteo(lat,lon):
    params={"latitude":lat,"longitude":lon,"current":"temperature_2m,precipitation,rain,wind_speed_10m","hourly":"precipitation_probability,precipitation,rain,wind_speed_10m","forecast_days":1,"timezone":"auto"}
    async with httpx.AsyncClient(timeout=10) as c:
        r=await c.get("https://api.open-meteo.com/v1/forecast",params=params); r.raise_for_status(); return r.json()
