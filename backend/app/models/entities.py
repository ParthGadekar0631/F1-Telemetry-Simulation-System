from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TelemetrySession(Base):
    __tablename__ = "telemetry_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(120))
    track_name: Mapped[str] = mapped_column(String(120))
    mode: Mapped[str] = mapped_column(String(20), default="live")
    status: Mapped[str] = mapped_column(String(20), default="running")
    total_laps: Mapped[int] = mapped_column(Integer, default=1)
    current_lap: Mapped[int] = mapped_column(Integer, default=1)
    configuration: Mapped[dict] = mapped_column(JSON, default=dict)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    latest_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    points: Mapped[list["TelemetryPoint"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    lap_summaries: Mapped[list["LapSummary"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    alerts: Mapped[list["TelemetryAlert"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    anomalies: Mapped[list["AnomalyEvent"]] = relationship(back_populates="session", cascade="all, delete-orphan")


class TelemetryPoint(Base):
    __tablename__ = "telemetry_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("telemetry_sessions.id"), index=True)
    lap_number: Mapped[int] = mapped_column(Integer, index=True)
    sector: Mapped[int] = mapped_column(Integer)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    track_x: Mapped[float] = mapped_column(Float)
    track_y: Mapped[float] = mapped_column(Float)
    lap_distance_pct: Mapped[float] = mapped_column(Float)
    speed_kph: Mapped[float] = mapped_column(Float)
    throttle_pct: Mapped[float] = mapped_column(Float)
    brake_pressure_bar: Mapped[float] = mapped_column(Float)
    rpm: Mapped[int] = mapped_column(Integer)
    gear: Mapped[int] = mapped_column(Integer)
    lap_time_ms: Mapped[int] = mapped_column(Integer)
    tire_temp_c: Mapped[float] = mapped_column(Float)
    engine_temp_c: Mapped[float] = mapped_column(Float)
    battery_pct: Mapped[float] = mapped_column(Float)
    battery_deployment_kw: Mapped[float] = mapped_column(Float)
    energy_used_kj: Mapped[float] = mapped_column(Float)
    fuel_load_kg: Mapped[float] = mapped_column(Float)

    session: Mapped["TelemetrySession"] = relationship(back_populates="points")


class LapSummary(Base):
    __tablename__ = "lap_summaries"
    __table_args__ = (UniqueConstraint("session_id", "lap_number", name="uq_lap_summary"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("telemetry_sessions.id"), index=True)
    lap_number: Mapped[int] = mapped_column(Integer, index=True)
    lap_time_ms: Mapped[int] = mapped_column(Integer)
    sector_1_ms: Mapped[int] = mapped_column(Integer)
    sector_2_ms: Mapped[int] = mapped_column(Integer)
    sector_3_ms: Mapped[int] = mapped_column(Integer)
    average_speed_kph: Mapped[float] = mapped_column(Float)
    top_speed_kph: Mapped[float] = mapped_column(Float)
    fuel_burn_kg: Mapped[float] = mapped_column(Float)
    energy_used_kj: Mapped[float] = mapped_column(Float)
    avg_tire_temp_c: Mapped[float] = mapped_column(Float)
    avg_engine_temp_c: Mapped[float] = mapped_column(Float)

    session: Mapped["TelemetrySession"] = relationship(back_populates="lap_summaries")
    sectors: Mapped[list["SectorSummary"]] = relationship(back_populates="lap_summary", cascade="all, delete-orphan")


class SectorSummary(Base):
    __tablename__ = "sector_summaries"
    __table_args__ = (UniqueConstraint("session_id", "lap_number", "sector_number", name="uq_sector_summary"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("telemetry_sessions.id"), index=True)
    lap_summary_id: Mapped[int | None] = mapped_column(ForeignKey("lap_summaries.id"), nullable=True)
    lap_number: Mapped[int] = mapped_column(Integer, index=True)
    sector_number: Mapped[int] = mapped_column(Integer)
    sector_time_ms: Mapped[int] = mapped_column(Integer)
    entry_speed_kph: Mapped[float] = mapped_column(Float)
    exit_speed_kph: Mapped[float] = mapped_column(Float)
    avg_throttle_pct: Mapped[float] = mapped_column(Float)
    max_brake_pressure_bar: Mapped[float] = mapped_column(Float)

    lap_summary: Mapped["LapSummary"] = relationship(back_populates="sectors")


class TelemetryAlert(Base):
    __tablename__ = "telemetry_alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("telemetry_sessions.id"), index=True)
    lap_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    severity: Mapped[str] = mapped_column(String(20))
    category: Mapped[str] = mapped_column(String(40))
    message: Mapped[str] = mapped_column(Text)
    metric_name: Mapped[str] = mapped_column(String(40))
    metric_value: Mapped[float] = mapped_column(Float)
    threshold_value: Mapped[float] = mapped_column(Float)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)

    session: Mapped["TelemetrySession"] = relationship(back_populates="alerts")


class AnomalyEvent(Base):
    __tablename__ = "anomaly_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("telemetry_sessions.id"), index=True)
    lap_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    anomaly_type: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(Text)
    metric_name: Mapped[str] = mapped_column(String(40))
    metric_value: Mapped[float] = mapped_column(Float)
    reference_value: Mapped[float] = mapped_column(Float)
    magnitude: Mapped[float] = mapped_column(Float)

    session: Mapped["TelemetrySession"] = relationship(back_populates="anomalies")


class ReplayMetadata(Base):
    __tablename__ = "replay_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("telemetry_sessions.id"), unique=True, index=True)
    source: Mapped[str] = mapped_column(String(30), default="simulator")
    total_points: Mapped[int] = mapped_column(Integer, default=0)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    available_laps: Mapped[list[int]] = mapped_column(JSON, default=list)
    default_replay_speed: Mapped[float] = mapped_column(Float, default=1.0)


class ExportHistory(Base):
    __tablename__ = "export_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("telemetry_sessions.id"), index=True)
    format: Mapped[str] = mapped_column(String(20))
    file_name: Mapped[str] = mapped_column(String(160))
    row_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
