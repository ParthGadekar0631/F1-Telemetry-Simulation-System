from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SessionStartRequest(BaseModel):
    name: str
    track_name: str
    total_laps: int = 1
    mode: str = "live"
    configuration: dict[str, Any] = Field(default_factory=dict)


class SessionStopRequest(BaseModel):
    status: str = "completed"


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: str
    name: str
    track_name: str
    mode: str
    status: str
    total_laps: int
    current_lap: int
    started_at: datetime
    ended_at: datetime | None = None


class SessionSummary(BaseModel):
    session_id: str
    name: str
    track_name: str
    circuit_id: str | None = None
    mode: str
    status: str
    total_laps: int
    current_lap: int
    weather_condition: str | None = None
    rain_intensity_pct: float | None = None
    wind_kph: float | None = None
    ambient_temp_c: float | None = None
    track_temp_c: float | None = None
    weather_phenomena: list[str] = Field(default_factory=list)
    best_lap_ms: int | None = None
    average_lap_ms: float | None = None
    total_alerts: int = 0
    total_anomalies: int = 0
    latest_timestamp: datetime | None = None
