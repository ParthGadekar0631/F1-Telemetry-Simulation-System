from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.replay import ReplayMetadataResponse, ReplayResponse
from app.schemas.telemetry import TelemetryPointResponse
from app.services.replay.service import ReplayService


router = APIRouter(prefix="/replay", tags=["replay"])
replay_service = ReplayService()


@router.get("/{session_id}", response_model=ReplayMetadataResponse)
def get_replay_metadata(session_id: str, db: Session = Depends(get_db)) -> ReplayMetadataResponse:
    metadata = replay_service.get_metadata(db, session_id)
    if metadata is None:
        raise HTTPException(status_code=404, detail="Replay metadata not found.")
    return ReplayMetadataResponse(
        session_id=session_id,
        total_points=metadata.total_points,
        duration_ms=metadata.duration_ms,
        available_laps=metadata.available_laps,
        default_replay_speed=metadata.default_replay_speed,
    )


@router.get("/{session_id}/laps/{lap_number}", response_model=ReplayResponse)
def get_replay_for_lap(session_id: str, lap_number: int, db: Session = Depends(get_db)) -> ReplayResponse:
    metadata = replay_service.get_metadata(db, session_id)
    if metadata is None:
        raise HTTPException(status_code=404, detail="Replay metadata not found.")

    points = replay_service.get_points(db, session_id, lap_number)
    return ReplayResponse(
        metadata=ReplayMetadataResponse(
            session_id=session_id,
            total_points=metadata.total_points,
            duration_ms=metadata.duration_ms,
            available_laps=metadata.available_laps,
            default_replay_speed=metadata.default_replay_speed,
        ),
        points=[TelemetryPointResponse.model_validate(point) for point in points],
        started_at=points[0].timestamp if points else None,
    )
