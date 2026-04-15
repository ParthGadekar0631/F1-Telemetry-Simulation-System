from statistics import mean

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import AnomalyEvent, LapSummary, SectorSummary, TelemetryAlert, TelemetryPoint, TelemetrySession
from app.schemas.analytics import (
    LapComparisonResponse,
    LapSummaryResponse,
    SectorComparisonResponse,
    SessionAnalyticsResponse,
)


class AnalyticsService:
    def build_lap_summary(self, db: Session, session_id: str, lap_number: int) -> LapSummary | None:
        points = list(
            db.scalars(
                select(TelemetryPoint)
                .where(TelemetryPoint.session_id == session_id, TelemetryPoint.lap_number == lap_number)
                .order_by(TelemetryPoint.timestamp.asc())
            )
        )
        if len(points) < 2:
            return None

        sector_times: dict[int, int] = {1: 0, 2: 0, 3: 0}
        for sector_number in (1, 2, 3):
            sector_points = [point for point in points if point.sector == sector_number]
            if sector_points:
                sector_times[sector_number] = sector_points[-1].lap_time_ms - sector_points[0].lap_time_ms

        existing = db.scalar(
            select(LapSummary).where(LapSummary.session_id == session_id, LapSummary.lap_number == lap_number)
        )
        if existing is None:
            existing = LapSummary(session_id=session_id, lap_number=lap_number)
            db.add(existing)

        existing.lap_time_ms = max(point.lap_time_ms for point in points)
        existing.sector_1_ms = sector_times[1]
        existing.sector_2_ms = sector_times[2]
        existing.sector_3_ms = sector_times[3]
        existing.average_speed_kph = mean(point.speed_kph for point in points)
        existing.top_speed_kph = max(point.speed_kph for point in points)
        existing.fuel_burn_kg = max(points[0].fuel_load_kg - points[-1].fuel_load_kg, 0.0)
        existing.energy_used_kj = max(points[-1].energy_used_kj - points[0].energy_used_kj, 0.0)
        existing.avg_tire_temp_c = mean(point.tire_temp_c for point in points)
        existing.avg_engine_temp_c = mean(point.engine_temp_c for point in points)

        for sector_number in (1, 2, 3):
            sector_points = [point for point in points if point.sector == sector_number]
            if not sector_points:
                continue

            sector_summary = db.scalar(
                select(SectorSummary).where(
                    SectorSummary.session_id == session_id,
                    SectorSummary.lap_number == lap_number,
                    SectorSummary.sector_number == sector_number,
                )
            )
            if sector_summary is None:
                sector_summary = SectorSummary(
                    session_id=session_id,
                    lap_number=lap_number,
                    sector_number=sector_number,
                )
                db.add(sector_summary)

            sector_summary.lap_summary = existing
            sector_summary.sector_time_ms = sector_times[sector_number]
            sector_summary.entry_speed_kph = sector_points[0].speed_kph
            sector_summary.exit_speed_kph = sector_points[-1].speed_kph
            sector_summary.avg_throttle_pct = mean(point.throttle_pct for point in sector_points)
            sector_summary.max_brake_pressure_bar = max(point.brake_pressure_bar for point in sector_points)

        return existing

    def session_analytics(self, db: Session, session_id: str) -> SessionAnalyticsResponse:
        lap_summaries = list(
            db.scalars(select(LapSummary).where(LapSummary.session_id == session_id).order_by(LapSummary.lap_number.asc()))
        )
        points = list(db.scalars(select(TelemetryPoint).where(TelemetryPoint.session_id == session_id)))

        best_lap = min(lap_summaries, key=lambda lap: lap.lap_time_ms, default=None)
        braking_zones = sum(1 for point in points if point.brake_pressure_bar >= 85)

        return SessionAnalyticsResponse(
            session_id=session_id,
            best_lap_number=best_lap.lap_number if best_lap else None,
            best_lap_ms=best_lap.lap_time_ms if best_lap else None,
            average_lap_ms=mean(lap.lap_time_ms for lap in lap_summaries) if lap_summaries else None,
            peak_speed_kph=max((point.speed_kph for point in points), default=None),
            total_energy_used_kj=sum(lap.energy_used_kj for lap in lap_summaries),
            total_fuel_burn_kg=sum(lap.fuel_burn_kg for lap in lap_summaries),
            average_engine_temp_c=mean(point.engine_temp_c for point in points) if points else None,
            average_tire_temp_c=mean(point.tire_temp_c for point in points) if points else None,
            braking_zones_detected=braking_zones,
            lap_summaries=[
                LapSummaryResponse(
                    lap_number=lap.lap_number,
                    lap_time_ms=lap.lap_time_ms,
                    sector_1_ms=lap.sector_1_ms,
                    sector_2_ms=lap.sector_2_ms,
                    sector_3_ms=lap.sector_3_ms,
                    average_speed_kph=lap.average_speed_kph,
                    top_speed_kph=lap.top_speed_kph,
                    fuel_burn_kg=lap.fuel_burn_kg,
                    energy_used_kj=lap.energy_used_kj,
                    avg_tire_temp_c=lap.avg_tire_temp_c,
                    avg_engine_temp_c=lap.avg_engine_temp_c,
                )
                for lap in lap_summaries
            ],
        )

    def compare_laps(self, db: Session, session_id: str, lap_a: int, lap_b: int) -> LapComparisonResponse:
        left = db.scalar(select(LapSummary).where(LapSummary.session_id == session_id, LapSummary.lap_number == lap_a))
        right = db.scalar(select(LapSummary).where(LapSummary.session_id == session_id, LapSummary.lap_number == lap_b))
        if left is None or right is None:
            raise ValueError("Requested laps do not exist for comparison.")

        return LapComparisonResponse(
            lap_a=lap_a,
            lap_b=lap_b,
            lap_a_time_ms=left.lap_time_ms,
            lap_b_time_ms=right.lap_time_ms,
            lap_delta_ms=right.lap_time_ms - left.lap_time_ms,
            sector_deltas_ms=[
                right.sector_1_ms - left.sector_1_ms,
                right.sector_2_ms - left.sector_2_ms,
                right.sector_3_ms - left.sector_3_ms,
            ],
            fuel_delta_kg=right.fuel_burn_kg - left.fuel_burn_kg,
            energy_delta_kj=right.energy_used_kj - left.energy_used_kj,
            top_speed_delta_kph=right.top_speed_kph - left.top_speed_kph,
        )

    def compare_sectors(self, db: Session, session_id: str, lap_a: int, lap_b: int) -> list[SectorComparisonResponse]:
        comparisons: list[SectorComparisonResponse] = []
        for sector_number in (1, 2, 3):
            left = db.scalar(
                select(SectorSummary).where(
                    SectorSummary.session_id == session_id,
                    SectorSummary.lap_number == lap_a,
                    SectorSummary.sector_number == sector_number,
                )
            )
            right = db.scalar(
                select(SectorSummary).where(
                    SectorSummary.session_id == session_id,
                    SectorSummary.lap_number == lap_b,
                    SectorSummary.sector_number == sector_number,
                )
            )
            if left is None or right is None:
                continue
            comparisons.append(
                SectorComparisonResponse(
                    sector_number=sector_number,
                    lap_a_time_ms=left.sector_time_ms,
                    lap_b_time_ms=right.sector_time_ms,
                    delta_ms=right.sector_time_ms - left.sector_time_ms,
                )
            )
        return comparisons
