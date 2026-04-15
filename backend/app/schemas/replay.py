from datetime import datetime

from pydantic import BaseModel

from app.schemas.telemetry import TelemetryPointResponse


class ReplayMetadataResponse(BaseModel):
    session_id: str
    total_points: int
    duration_ms: int
    available_laps: list[int]
    default_replay_speed: float


class ReplayResponse(BaseModel):
    metadata: ReplayMetadataResponse
    points: list[TelemetryPointResponse]
    started_at: datetime | None = None
