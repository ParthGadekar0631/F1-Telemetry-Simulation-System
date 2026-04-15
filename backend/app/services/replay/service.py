from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ReplayMetadata, TelemetryPoint


class ReplayService:
    def get_metadata(self, db: Session, session_id: str) -> ReplayMetadata | None:
        return db.scalar(select(ReplayMetadata).where(ReplayMetadata.session_id == session_id))

    def get_points(self, db: Session, session_id: str, lap_number: int | None = None) -> list[TelemetryPoint]:
        query = select(TelemetryPoint).where(TelemetryPoint.session_id == session_id)
        if lap_number is not None:
            query = query.where(TelemetryPoint.lap_number == lap_number)
        return list(db.scalars(query.order_by(TelemetryPoint.timestamp.asc())))
