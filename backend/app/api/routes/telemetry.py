from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.models import TelemetryPoint
from app.schemas.telemetry import LiveTelemetryResponse, TelemetryIngestRequest, TelemetryPointResponse
from app.services.ingestion.service import IngestionService


router = APIRouter(prefix="/telemetry", tags=["telemetry"])
ingestion_service = IngestionService()
settings = get_settings()


@router.post("/ingest")
def ingest_telemetry(payload: TelemetryIngestRequest, db: Session = Depends(get_db)) -> dict[str, int]:
    try:
        count = ingestion_service.ingest(db, payload)
        return {"ingested": count}
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/live", response_model=LiveTelemetryResponse)
def get_live_telemetry(session_id: str, db: Session = Depends(get_db)) -> LiveTelemetryResponse:
    latest = db.scalar(
        select(TelemetryPoint)
        .where(TelemetryPoint.session_id == session_id)
        .order_by(TelemetryPoint.timestamp.desc())
    )
    if latest is None:
        return LiveTelemetryResponse(session_id=session_id, is_live=False, latest=None, updated_at=None)

    age = datetime.now(timezone.utc) - latest.timestamp.replace(tzinfo=timezone.utc)
    return LiveTelemetryResponse(
        session_id=session_id,
        is_live=age <= timedelta(seconds=settings.live_stale_seconds),
        latest=TelemetryPointResponse.model_validate(latest),
        updated_at=latest.timestamp,
    )


@router.get("/latest/{session_id}", response_model=TelemetryPointResponse)
def get_latest_telemetry(session_id: str, db: Session = Depends(get_db)) -> TelemetryPointResponse:
    latest = db.scalar(
        select(TelemetryPoint)
        .where(TelemetryPoint.session_id == session_id)
        .order_by(TelemetryPoint.timestamp.desc())
    )
    if latest is None:
        raise HTTPException(status_code=404, detail="No telemetry points found.")
    return TelemetryPointResponse.model_validate(latest)


@router.get("/history/{session_id}", response_model=list[TelemetryPointResponse])
def get_history_for_lap(
    session_id: str,
    lap_number: int | None = None,
    start: datetime | None = Query(default=None),
    end: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[TelemetryPointResponse]:
    query = select(TelemetryPoint).where(TelemetryPoint.session_id == session_id)
    if lap_number is not None:
        query = query.where(TelemetryPoint.lap_number == lap_number)
    if start is not None:
        query = query.where(TelemetryPoint.timestamp >= start)
    if end is not None:
        query = query.where(TelemetryPoint.timestamp <= end)
    points = list(db.scalars(query.order_by(TelemetryPoint.timestamp.asc())))
    return [TelemetryPointResponse.model_validate(point) for point in points]
