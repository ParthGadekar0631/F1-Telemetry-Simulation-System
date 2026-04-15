from datetime import timezone

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models import ReplayMetadata, TelemetryPoint, TelemetrySession
from app.schemas.telemetry import TelemetryIngestRequest, TelemetryPointIn
from app.services.alerts.service import AlertService
from app.services.analytics.service import AnalyticsService


class IngestionService:
    def __init__(self) -> None:
        self.alerts = AlertService()
        self.analytics = AnalyticsService()

    def ingest(self, db: Session, payload: TelemetryIngestRequest) -> int:
        session = db.get(TelemetrySession, payload.session_id)
        if session is None:
            raise ValueError("Session not found.")

        previous_model = db.scalar(
            select(TelemetryPoint)
            .where(TelemetryPoint.session_id == payload.session_id)
            .order_by(desc(TelemetryPoint.timestamp))
        )
        previous_point = None
        if previous_model is not None:
            previous_point = TelemetryPointIn(
                session_id=previous_model.session_id,
                lap_number=previous_model.lap_number,
                sector=previous_model.sector,
                timestamp=previous_model.timestamp,
                track_x=previous_model.track_x,
                track_y=previous_model.track_y,
                lap_distance_pct=previous_model.lap_distance_pct,
                speed_kph=previous_model.speed_kph,
                throttle_pct=previous_model.throttle_pct,
                brake_pressure_bar=previous_model.brake_pressure_bar,
                rpm=previous_model.rpm,
                gear=previous_model.gear,
                lap_time_ms=previous_model.lap_time_ms,
                tire_temp_c=previous_model.tire_temp_c,
                engine_temp_c=previous_model.engine_temp_c,
                battery_pct=previous_model.battery_pct,
                battery_deployment_kw=previous_model.battery_deployment_kw,
                energy_used_kj=previous_model.energy_used_kj,
                fuel_load_kg=previous_model.fuel_load_kg,
            )

        affected_laps: set[int] = set()
        for point in payload.points:
            db.add(
                TelemetryPoint(
                    session_id=payload.session_id,
                    lap_number=point.lap_number,
                    sector=point.sector,
                    timestamp=point.timestamp,
                    track_x=point.track_x,
                    track_y=point.track_y,
                    lap_distance_pct=point.lap_distance_pct,
                    speed_kph=point.speed_kph,
                    throttle_pct=point.throttle_pct,
                    brake_pressure_bar=point.brake_pressure_bar,
                    rpm=point.rpm,
                    gear=point.gear,
                    lap_time_ms=point.lap_time_ms,
                    tire_temp_c=point.tire_temp_c,
                    engine_temp_c=point.engine_temp_c,
                    battery_pct=point.battery_pct,
                    battery_deployment_kw=point.battery_deployment_kw,
                    energy_used_kj=point.energy_used_kj,
                    fuel_load_kg=point.fuel_load_kg,
                )
            )

            alerts, anomalies = self.alerts.evaluate(point, previous_point)
            for alert in alerts:
                db.add(alert)
            for anomaly in anomalies:
                db.add(anomaly)

            previous_point = point
            affected_laps.add(point.lap_number)
            session.current_lap = max(session.current_lap, point.lap_number)
            session.latest_timestamp = point.timestamp

        metadata = db.scalar(select(ReplayMetadata).where(ReplayMetadata.session_id == payload.session_id))
        if metadata is None:
            metadata = ReplayMetadata(
                session_id=payload.session_id,
                source="simulator",
                total_points=0,
                duration_ms=0,
                available_laps=[],
                default_replay_speed=float(session.configuration.get("replay_speed", 1.0)),
            )
            db.add(metadata)

        metadata.total_points += len(payload.points)
        metadata.available_laps = sorted(set([*metadata.available_laps, *affected_laps]))
        if payload.points:
            started_at = session.started_at
            if started_at.tzinfo is None:
                started_at = started_at.replace(tzinfo=timezone.utc)
            metadata.duration_ms = max(
                metadata.duration_ms,
                int((payload.points[-1].timestamp - started_at).total_seconds() * 1000),
            )

        db.flush()

        for lap_number in affected_laps:
            if lap_number < session.current_lap or session.status != "running":
                self.analytics.build_lap_summary(db, payload.session_id, lap_number)

        db.commit()
        return len(payload.points)

    def finalize_session(self, db: Session, session_id: str) -> None:
        session = db.get(TelemetrySession, session_id)
        if session is None:
            raise ValueError("Session not found.")

        max_lap = db.scalar(
            select(TelemetryPoint.lap_number)
            .where(TelemetryPoint.session_id == session_id)
            .order_by(desc(TelemetryPoint.lap_number))
        )
        if max_lap is not None:
            for lap_number in range(1, max_lap + 1):
                self.analytics.build_lap_summary(db, session_id, lap_number)

        db.commit()
