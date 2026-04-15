import os
from collections.abc import Generator
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

os.environ["DATABASE_URL"] = "sqlite:///./test_f1_telemetry.db"

from app.db.base import Base
from app.db.session import get_db
from app.main import app


engine = create_engine(
    os.environ["DATABASE_URL"],
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_database() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def telemetry_points_factory():
    def build(session_id: str, lap_number: int, offset_seconds: int = 0, hot: bool = False) -> list[dict]:
        base_time = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc) + timedelta(seconds=offset_seconds)
        return [
            {
                "session_id": session_id,
                "lap_number": lap_number,
                "sector": 1,
                "timestamp": base_time.isoformat(),
                "track_x": 10.0,
                "track_y": 20.0,
                "lap_distance_pct": 0.10,
                "speed_kph": 160.0,
                "throttle_pct": 82.0,
                "brake_pressure_bar": 4.0,
                "rpm": 12800,
                "gear": 5,
                "lap_time_ms": 10000,
                "tire_temp_c": 111.0 if hot else 94.0,
                "engine_temp_c": 121.0 if hot else 103.0,
                "battery_pct": 72.0,
                "battery_deployment_kw": 280.0,
                "energy_used_kj": float(30 * lap_number),
                "fuel_load_kg": 7.5 if hot else 78.0 - lap_number,
            },
            {
                "session_id": session_id,
                "lap_number": lap_number,
                "sector": 2,
                "timestamp": (base_time + timedelta(seconds=1)).isoformat(),
                "track_x": 40.0,
                "track_y": 35.0,
                "lap_distance_pct": 0.48,
                "speed_kph": 220.0,
                "throttle_pct": 94.0,
                "brake_pressure_bar": 112.0 if hot else 18.0,
                "rpm": 14400,
                "gear": 7,
                "lap_time_ms": 40000,
                "tire_temp_c": 114.0 if hot else 98.0,
                "engine_temp_c": 123.0 if hot else 105.0,
                "battery_pct": 69.0 if hot else 71.2,
                "battery_deployment_kw": 335.0,
                "energy_used_kj": float(80 * lap_number),
                "fuel_load_kg": 6.8 if hot else 77.1 - lap_number,
            },
            {
                "session_id": session_id,
                "lap_number": lap_number,
                "sector": 3,
                "timestamp": (base_time + timedelta(seconds=2)).isoformat(),
                "track_x": 60.0,
                "track_y": 52.0,
                "lap_distance_pct": 0.97,
                "speed_kph": 305.0 if lap_number == 1 else 298.0,
                "throttle_pct": 100.0,
                "brake_pressure_bar": 12.0,
                "rpm": 15100,
                "gear": 8,
                "lap_time_ms": 90000 if lap_number == 1 else 91500,
                "tire_temp_c": 106.0 if hot else 99.0,
                "engine_temp_c": 115.0 if hot else 104.0,
                "battery_pct": 67.0 if hot else 70.3,
                "battery_deployment_kw": 340.0,
                "energy_used_kj": float(140 * lap_number),
                "fuel_load_kg": 6.0 if hot else 76.2 - lap_number,
            },
        ]

    return build
