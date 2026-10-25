from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from .config import settings
from .db import get_db
from .schemas import HealthResponse, EmptyCollection, DashboardSummary

app = FastAPI(title="FRA Atlas API", version="0.1.0",
              description="FRA Atlas API. Responses remain empty until verified datasets are imported.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.get("/api/health", response_model=HealthResponse)
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "ok", "database": "unavailable"}

@app.get("/api/states", response_model=EmptyCollection)
def states(db: Session = Depends(get_db)):
    return {"items": [], "total": 0, "source_status": "not_connected"}

@app.get("/api/districts", response_model=EmptyCollection)
def districts(state_id: str | None = None, db: Session = Depends(get_db)):
    return {"items": [], "total": 0, "source_status": "not_connected"}

@app.get("/api/locations", response_model=EmptyCollection)
def locations(state: str | None = None, district: str | None = None,
              block: str | None = None, q: str | None = None,
              db: Session = Depends(get_db)):
    return {"items": [], "total": 0, "source_status": "not_connected"}

@app.get("/api/dashboard/summary", response_model=DashboardSummary)
def summary(state: str | None = None, district: str | None = None,
            block: str | None = None, village: str | None = None,
            db: Session = Depends(get_db)):
    return DashboardSummary(state=state, district=district, block=block,
                            village=village, source_status="not_connected")

@app.get("/api/statistics", response_model=EmptyCollection)
def statistics(state: str | None = None, district: str | None = None,
               reporting_date: str | None = None, db: Session = Depends(get_db)):
    return {"items": [], "total": 0, "source_status": "not_connected"}

@app.get("/api/statistics/trends", response_model=EmptyCollection)
def trends(state: str | None = None, district: str | None = None,
           db: Session = Depends(get_db)):
    return {"items": [], "total": 0, "source_status": "not_connected"}

@app.get("/api/map/districts", response_model=EmptyCollection)
def map_districts(state: str | None = None, db: Session = Depends(get_db)):
    # Return GeoJSON features here once verified district geometry is imported.
    return {"items": [], "total": 0, "source_status": "not_connected"}

@app.get("/api/map/claims", response_model=EmptyCollection)
def map_claims(state: str | None = None, district: str | None = None,
               db: Session = Depends(get_db)):
    return {"items": [], "total": 0, "source_status": "not_connected"}

@app.get("/api/data-sources", response_model=EmptyCollection)
def data_sources(db: Session = Depends(get_db)):
    return {"items": [], "total": 0, "source_status": "not_connected"}

@app.get("/api/insights", response_model=EmptyCollection)
def insights(state: str | None = None, district: str | None = None,
             db: Session = Depends(get_db)):
    return {"items": [], "total": 0, "source_status": "not_connected"}

@app.get("/api/schemes/eligibility", response_model=EmptyCollection)
def scheme_eligibility(state: str | None = None, district: str | None = None,
                       village: str | None = None, db: Session = Depends(get_db)):
    return {"items": [], "total": 0, "source_status": "not_connected"}
