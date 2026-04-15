import csv
import io
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ExportHistory, LapSummary, TelemetryPoint


class ExportService:
    def export_session(self, db: Session, session_id: str, export_format: str) -> tuple[str, str]:
        points = list(
            db.scalars(
                select(TelemetryPoint)
                .where(TelemetryPoint.session_id == session_id)
                .order_by(TelemetryPoint.timestamp.asc())
            )
        )
        lap_summaries = list(
            db.scalars(
                select(LapSummary).where(LapSummary.session_id == session_id).order_by(LapSummary.lap_number.asc())
            )
        )

        if export_format == "json":
            payload = {
                "session_id": session_id,
                "points": [
                    {
                        "timestamp": point.timestamp.isoformat(),
                        "lap_number": point.lap_number,
                        "sector": point.sector,
                        "track_x": point.track_x,
                        "track_y": point.track_y,
                        "lap_distance_pct": point.lap_distance_pct,
                        "speed_kph": point.speed_kph,
                        "throttle_pct": point.throttle_pct,
                        "brake_pressure_bar": point.brake_pressure_bar,
                        "rpm": point.rpm,
                        "gear": point.gear,
                        "lap_time_ms": point.lap_time_ms,
                        "tire_temp_c": point.tire_temp_c,
                        "engine_temp_c": point.engine_temp_c,
                        "battery_pct": point.battery_pct,
                        "battery_deployment_kw": point.battery_deployment_kw,
                        "energy_used_kj": point.energy_used_kj,
                        "fuel_load_kg": point.fuel_load_kg,
                    }
                    for point in points
                ],
                "lap_summaries": [
                    {
                        "lap_number": lap.lap_number,
                        "lap_time_ms": lap.lap_time_ms,
                        "sector_1_ms": lap.sector_1_ms,
                        "sector_2_ms": lap.sector_2_ms,
                        "sector_3_ms": lap.sector_3_ms,
                        "average_speed_kph": lap.average_speed_kph,
                        "top_speed_kph": lap.top_speed_kph,
                    }
                    for lap in lap_summaries
                ],
            }
            content = json.dumps(payload, indent=2)
            media_type = "application/json"
            file_name = f"{session_id}.json"
        else:
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(
                [
                    "timestamp",
                    "lap_number",
                    "sector",
                    "track_x",
                    "track_y",
                    "speed_kph",
                    "throttle_pct",
                    "brake_pressure_bar",
                    "rpm",
                    "gear",
                    "lap_time_ms",
                    "tire_temp_c",
                    "engine_temp_c",
                    "battery_pct",
                    "battery_deployment_kw",
                    "energy_used_kj",
                    "fuel_load_kg",
                    "lap_distance_pct",
                ]
            )
            for point in points:
                writer.writerow(
                    [
                        point.timestamp.isoformat(),
                        point.lap_number,
                        point.sector,
                        point.track_x,
                        point.track_y,
                        point.speed_kph,
                        point.throttle_pct,
                        point.brake_pressure_bar,
                        point.rpm,
                        point.gear,
                        point.lap_time_ms,
                        point.tire_temp_c,
                        point.engine_temp_c,
                        point.battery_pct,
                        point.battery_deployment_kw,
                        point.energy_used_kj,
                        point.fuel_load_kg,
                        point.lap_distance_pct,
                    ]
                )
            content = buffer.getvalue()
            media_type = "text/csv"
            file_name = f"{session_id}.csv"

        db.add(
            ExportHistory(
                session_id=session_id,
                format=export_format,
                file_name=file_name,
                row_count=len(points),
            )
        )
        db.commit()
        return content, media_type
