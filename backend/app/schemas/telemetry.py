from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TelemetryPointIn(BaseModel):
    session_id: str
    lap_number: int
    sector: int
    timestamp: datetime
    track_x: float
    track_y: float
    lap_distance_pct: float
    speed_kph: float
    throttle_pct: float
    brake_pressure_bar: float
    rpm: int
    gear: int
    lap_time_ms: int
    tire_temp_c: float
    engine_temp_c: float
    battery_pct: float
    battery_deployment_kw: float
    energy_used_kj: float
    fuel_load_kg: float


class TelemetryIngestRequest(BaseModel):
    session_id: str
    points: list[TelemetryPointIn] = Field(default_factory=list)


class TelemetryPointResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: str
    lap_number: int
    sector: int
    timestamp: datetime
    track_x: float
    track_y: float
    lap_distance_pct: float
    speed_kph: float
    throttle_pct: float
    brake_pressure_bar: float
    rpm: int
    gear: int
    lap_time_ms: int
    tire_temp_c: float
    engine_temp_c: float
    battery_pct: float
    battery_deployment_kw: float
    energy_used_kj: float
    fuel_load_kg: float


class LiveTelemetryResponse(BaseModel):
    session_id: str
    is_live: bool
    latest: TelemetryPointResponse | None
    updated_at: datetime | None = None
