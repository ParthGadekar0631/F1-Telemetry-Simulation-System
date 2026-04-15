from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analytics import LapComparisonResponse, SectorComparisonResponse, SessionAnalyticsResponse
from app.services.analytics.service import AnalyticsService


router = APIRouter(prefix="/analytics", tags=["analytics"])
analytics_service = AnalyticsService()


@router.get("/sessions/{session_id}/summary", response_model=SessionAnalyticsResponse)
def get_session_summary(session_id: str, db: Session = Depends(get_db)) -> SessionAnalyticsResponse:
    return analytics_service.session_analytics(db, session_id)


@router.get("/sessions/{session_id}/laps/compare", response_model=LapComparisonResponse)
def compare_laps(session_id: str, lap_a: int, lap_b: int, db: Session = Depends(get_db)) -> LapComparisonResponse:
    try:
        return analytics_service.compare_laps(db, session_id, lap_a, lap_b)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/sessions/{session_id}/sectors/compare", response_model=list[SectorComparisonResponse])
def compare_sectors(session_id: str, lap_a: int, lap_b: int, db: Session = Depends(get_db)) -> list[SectorComparisonResponse]:
    return analytics_service.compare_sectors(db, session_id, lap_a, lap_b)
