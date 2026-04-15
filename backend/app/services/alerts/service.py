from datetime import datetime

from app.models import AnomalyEvent, TelemetryAlert
from app.schemas.telemetry import TelemetryPointIn


class AlertService:
    def evaluate(
        self,
        point: TelemetryPointIn,
        previous_point: TelemetryPointIn | None = None,
    ) -> tuple[list[TelemetryAlert], list[AnomalyEvent]]:
        alerts: list[TelemetryAlert] = []
        anomalies: list[AnomalyEvent] = []

        if point.engine_temp_c >= 118:
            alerts.append(
                TelemetryAlert(
                    session_id=point.session_id,
                    lap_number=point.lap_number,
                    timestamp=point.timestamp,
                    severity="critical",
                    category="thermal",
                    message="Engine temperature exceeds safe operating window.",
                    metric_name="engine_temp_c",
                    metric_value=point.engine_temp_c,
                    threshold_value=118.0,
                )
            )

        if point.tire_temp_c >= 110:
            alerts.append(
                TelemetryAlert(
                    session_id=point.session_id,
                    lap_number=point.lap_number,
                    timestamp=point.timestamp,
                    severity="warning",
                    category="tire",
                    message="Tire surface temperature is trending too high.",
                    metric_name="tire_temp_c",
                    metric_value=point.tire_temp_c,
                    threshold_value=110.0,
                )
            )

        if point.fuel_load_kg <= 8:
            alerts.append(
                TelemetryAlert(
                    session_id=point.session_id,
                    lap_number=point.lap_number,
                    timestamp=point.timestamp,
                    severity="warning",
                    category="fuel",
                    message="Fuel reserve is below the configured low-fuel threshold.",
                    metric_name="fuel_load_kg",
                    metric_value=point.fuel_load_kg,
                    threshold_value=8.0,
                )
            )

        if point.brake_pressure_bar >= 108:
            alerts.append(
                TelemetryAlert(
                    session_id=point.session_id,
                    lap_number=point.lap_number,
                    timestamp=point.timestamp,
                    severity="warning",
                    category="braking",
                    message="Brake pressure indicates an extreme braking event.",
                    metric_name="brake_pressure_bar",
                    metric_value=point.brake_pressure_bar,
                    threshold_value=108.0,
                )
            )

        if previous_point is None:
            return alerts, anomalies

        speed_drop = previous_point.speed_kph - point.speed_kph
        if speed_drop >= 75 and point.brake_pressure_bar < 20:
            anomalies.append(
                AnomalyEvent(
                    session_id=point.session_id,
                    lap_number=point.lap_number,
                    timestamp=point.timestamp,
                    anomaly_type="sudden_speed_drop",
                    description="Vehicle speed dropped sharply without a matching braking input.",
                    metric_name="speed_kph",
                    metric_value=point.speed_kph,
                    reference_value=previous_point.speed_kph,
                    magnitude=speed_drop,
                )
            )

        battery_drop = previous_point.battery_pct - point.battery_pct
        if battery_drop >= 1.4:
            anomalies.append(
                AnomalyEvent(
                    session_id=point.session_id,
                    lap_number=point.lap_number,
                    timestamp=point.timestamp,
                    anomaly_type="battery_usage_spike",
                    description="Battery state-of-charge dropped faster than expected for the sample interval.",
                    metric_name="battery_pct",
                    metric_value=point.battery_pct,
                    reference_value=previous_point.battery_pct,
                    magnitude=battery_drop,
                )
            )

        thermal_rise = point.engine_temp_c - previous_point.engine_temp_c
        if thermal_rise >= 3.5:
            anomalies.append(
                AnomalyEvent(
                    session_id=point.session_id,
                    lap_number=point.lap_number,
                    timestamp=point.timestamp,
                    anomaly_type="engine_temp_spike",
                    description="Engine temperature increased abnormally between successive telemetry packets.",
                    metric_name="engine_temp_c",
                    metric_value=point.engine_temp_c,
                    reference_value=previous_point.engine_temp_c,
                    magnitude=thermal_rise,
                )
            )

        return alerts, anomalies
