from pydantic import BaseModel
from typing import Any

class HealthResponse(BaseModel):
    status: str
    database: str

class EmptyCollection(BaseModel):
    items: list[dict[str, Any]]
    total: int = 0
    source_status: str = "not_connected"

class DashboardSummary(BaseModel):
    state: str | None = None
    district: str | None = None
    block: str | None = None
    village: str | None = None
    reporting_date: str | None = None
    claims_received: int | None = None
    claims_approved: int | None = None
    claims_pending: int | None = None
    claims_rejected: int | None = None
    approval_rate: float | None = None
    population: int | None = None
    households: int | None = None
    forest_area_ha: float | None = None
    agricultural_land_ha: float | None = None
    source_status: str = "not_connected"
