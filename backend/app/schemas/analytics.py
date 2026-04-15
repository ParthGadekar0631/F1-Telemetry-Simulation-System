from pydantic import BaseModel


class LapSummaryResponse(BaseModel):
    lap_number: int
    lap_time_ms: int
    sector_1_ms: int
    sector_2_ms: int
    sector_3_ms: int
    average_speed_kph: float
    top_speed_kph: float
    fuel_burn_kg: float
    energy_used_kj: float
    avg_tire_temp_c: float
    avg_engine_temp_c: float


class SectorComparisonResponse(BaseModel):
    sector_number: int
    lap_a_time_ms: int
    lap_b_time_ms: int
    delta_ms: int


class LapComparisonResponse(BaseModel):
    lap_a: int
    lap_b: int
    lap_a_time_ms: int
    lap_b_time_ms: int
    lap_delta_ms: int
    sector_deltas_ms: list[int]
    fuel_delta_kg: float
    energy_delta_kj: float
    top_speed_delta_kph: float


class SessionAnalyticsResponse(BaseModel):
    session_id: str
    best_lap_number: int | None = None
    best_lap_ms: int | None = None
    average_lap_ms: float | None = None
    peak_speed_kph: float | None = None
    total_energy_used_kj: float
    total_fuel_burn_kg: float
    average_engine_temp_c: float | None = None
    average_tire_temp_c: float | None = None
    braking_zones_detected: int
    lap_summaries: list[LapSummaryResponse]
