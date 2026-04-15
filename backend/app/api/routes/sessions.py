from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import AnomalyEvent, LapSummary, TelemetryAlert, TelemetrySession
from app.schemas.session import SessionResponse, SessionStartRequest, SessionStopRequest, SessionSummary
from app.services.ingestion.service import IngestionService


router = APIRouter(prefix="/sessions", tags=["sessions"])
ingestion_service = IngestionService()


@router.post("/start", response_model=SessionResponse)
def start_session(payload: SessionStartRequest, db: Session = Depends(get_db)) -> SessionResponse:
    session = TelemetrySession(
        name=payload.name,
        track_name=payload.track_name,
        total_laps=payload.total_laps,
        mode=payload.mode,
        status="running",
        configuration=payload.configuration,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return SessionResponse(
        session_id=session.id,
        name=session.name,
        track_name=session.track_name,
        mode=session.mode,
        status=session.status,
        total_laps=session.total_laps,
        current_lap=session.current_lap,
        started_at=session.started_at,
        ended_at=session.ended_at,
    )


@router.post("/{session_id}/stop", response_model=SessionResponse)
def stop_session(session_id: str, payload: SessionStopRequest, db: Session = Depends(get_db)) -> SessionResponse:
    session = db.get(TelemetrySession, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    session.status = payload.status
    session.ended_at = datetime.now(timezone.utc)
    ingestion_service.finalize_session(db, session_id)
    db.commit()
    db.refresh(session)

    return SessionResponse(
        session_id=session.id,
        name=session.name,
        track_name=session.track_name,
        mode=session.mode,
        status=session.status,
        total_laps=session.total_laps,
        current_lap=session.current_lap,
        started_at=session.started_at,
        ended_at=session.ended_at,
    )


@router.get("", response_model=list[SessionSummary])
def list_sessions(db: Session = Depends(get_db)) -> list[SessionSummary]:
    sessions = list(db.scalars(select(TelemetrySession).order_by(TelemetrySession.started_at.desc())))
    results: list[SessionSummary] = []
    for session in sessions:
        best_lap = db.scalar(
            select(func.min(LapSummary.lap_time_ms)).where(LapSummary.session_id == session.id)
        )
        average_lap = db.scalar(
            select(func.avg(LapSummary.lap_time_ms)).where(LapSummary.session_id == session.id)
        )
        total_alerts = db.scalar(
            select(func.count(TelemetryAlert.id)).where(TelemetryAlert.session_id == session.id)
        ) or 0
        total_anomalies = db.scalar(
            select(func.count(AnomalyEvent.id)).where(AnomalyEvent.session_id == session.id)
        ) or 0
        results.append(
            SessionSummary(
                session_id=session.id,
                name=session.name,
                track_name=session.track_name,
                circuit_id=session.configuration.get("circuit_id"),
                mode=session.mode,
                status=session.status,
                total_laps=session.total_laps,
                current_lap=session.current_lap,
                weather_condition=session.configuration.get("weather", {}).get("condition"),
                rain_intensity_pct=session.configuration.get("weather", {}).get("rain_intensity_pct"),
                wind_kph=session.configuration.get("weather", {}).get("wind_kph"),
                ambient_temp_c=session.configuration.get("weather", {}).get("ambient_temp_c"),
                track_temp_c=session.configuration.get("weather", {}).get("track_temp_c"),
                weather_phenomena=session.configuration.get("weather", {}).get("phenomena", []),
                best_lap_ms=best_lap,
                average_lap_ms=float(average_lap) if average_lap is not None else None,
                total_alerts=total_alerts,
                total_anomalies=total_anomalies,
                latest_timestamp=session.latest_timestamp,
            )
        )
    return results
