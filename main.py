from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router

app = FastAPI(title="PATHSAFE AI API", version="0.1.0", description="Uncertainty-aware disaster routing research MVP")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"name":"PATHSAFE AI","status":"ok","message":"Find the safer way out."}
