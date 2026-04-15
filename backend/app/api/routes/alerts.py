from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import AnomalyEvent, TelemetryAlert
from app.schemas.alerts import AlertResponse, AnomalyResponse


router = APIRouter(tags=["alerts"])


@router.get("/alerts", response_model=list[AlertResponse])
def get_alerts(session_id: str, db: Session = Depends(get_db)) -> list[AlertResponse]:
    alerts = list(
        db.scalars(
            select(TelemetryAlert)
            .where(TelemetryAlert.session_id == session_id)
            .order_by(TelemetryAlert.timestamp.desc())
        )
    )
    return [AlertResponse.model_validate(alert) for alert in alerts]


@router.get("/anomalies", response_model=list[AnomalyResponse])
def get_anomalies(session_id: str, db: Session = Depends(get_db)) -> list[AnomalyResponse]:
    anomalies = list(
        db.scalars(
            select(AnomalyEvent)
            .where(AnomalyEvent.session_id == session_id)
            .order_by(AnomalyEvent.timestamp.desc())
        )
    )
    return [AnomalyResponse.model_validate(item) for item in anomalies]
