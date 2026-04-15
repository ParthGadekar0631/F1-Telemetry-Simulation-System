import json
import math
import random
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


API_BASE = "http://localhost:8000/api/v1"
POINTS_PER_LAP = 9


@dataclass(frozen=True)
class RaceSeed:
    event_name: str
    track_name: str
    circuit_id: str
    laps: int
    weather: dict


RACES_2026 = [
    RaceSeed("Australian Grand Prix", "Albert Park", "albert-park", 58, {"condition": "Dry", "rain_intensity_pct": 0, "wind_kph": 11, "ambient_temp_c": 24, "track_temp_c": 36, "phenomena": ["gusty coastal wind"]}),
    RaceSeed("Chinese Grand Prix", "Shanghai International Circuit", "shanghai", 56, {"condition": "Cloudy", "rain_intensity_pct": 10, "wind_kph": 14, "ambient_temp_c": 21, "track_temp_c": 30, "phenomena": ["low cloud cover"]}),
    RaceSeed("Japanese Grand Prix", "Suzuka Circuit", "suzuka", 53, {"condition": "Mixed", "rain_intensity_pct": 22, "wind_kph": 18, "ambient_temp_c": 20, "track_temp_c": 28, "phenomena": ["crosswind through S curves"]}),
    RaceSeed("Bahrain Grand Prix", "Bahrain International Circuit", "bahrain", 57, {"condition": "Hot", "rain_intensity_pct": 0, "wind_kph": 16, "ambient_temp_c": 31, "track_temp_c": 43, "phenomena": ["dust haze"]}),
    RaceSeed("Saudi Arabian Grand Prix", "Jeddah Corniche Circuit", "jeddah", 50, {"condition": "Clear Night", "rain_intensity_pct": 0, "wind_kph": 15, "ambient_temp_c": 27, "track_temp_c": 34, "phenomena": ["marine humidity"]}),
    RaceSeed("Miami Grand Prix", "Miami International Autodrome", "miami", 57, {"condition": "Humid", "rain_intensity_pct": 14, "wind_kph": 13, "ambient_temp_c": 29, "track_temp_c": 40, "phenomena": ["heat haze", "intermittent shower risk"]}),
    RaceSeed("Canadian Grand Prix", "Circuit Gilles Villeneuve", "montreal", 70, {"condition": "Variable", "rain_intensity_pct": 18, "wind_kph": 17, "ambient_temp_c": 22, "track_temp_c": 31, "phenomena": ["tailwind on straights"]}),
    RaceSeed("Monaco Grand Prix", "Circuit de Monaco", "monaco", 78, {"condition": "Dry", "rain_intensity_pct": 0, "wind_kph": 7, "ambient_temp_c": 23, "track_temp_c": 34, "phenomena": ["shade variation"]}),
    RaceSeed("Barcelona-Catalunya Grand Prix", "Circuit de Barcelona-Catalunya", "barcelona", 66, {"condition": "Sunny", "rain_intensity_pct": 0, "wind_kph": 21, "ambient_temp_c": 28, "track_temp_c": 41, "phenomena": ["strong turn-9 crosswind"]}),
    RaceSeed("Austrian Grand Prix", "Red Bull Ring", "red-bull-ring", 71, {"condition": "Mountain Breeze", "rain_intensity_pct": 12, "wind_kph": 22, "ambient_temp_c": 20, "track_temp_c": 29, "phenomena": ["elevation gusts"]}),
    RaceSeed("British Grand Prix", "Silverstone Circuit", "silverstone", 52, {"condition": "Mixed", "rain_intensity_pct": 25, "wind_kph": 24, "ambient_temp_c": 19, "track_temp_c": 27, "phenomena": ["rapid weather shifts"]}),
    RaceSeed("Belgian Grand Prix", "Spa-Francorchamps", "spa", 44, {"condition": "Wet Patches", "rain_intensity_pct": 35, "wind_kph": 19, "ambient_temp_c": 18, "track_temp_c": 23, "phenomena": ["localized showers", "forest mist"]}),
    RaceSeed("Hungarian Grand Prix", "Hungaroring", "hungaroring", 70, {"condition": "Hot", "rain_intensity_pct": 0, "wind_kph": 9, "ambient_temp_c": 30, "track_temp_c": 45, "phenomena": ["heat soak"]}),
    RaceSeed("Dutch Grand Prix", "Zandvoort", "zandvoort", 72, {"condition": "Breezy", "rain_intensity_pct": 8, "wind_kph": 26, "ambient_temp_c": 22, "track_temp_c": 30, "phenomena": ["sand blow", "coastal gusts"]}),
    RaceSeed("Italian Grand Prix", "Autodromo Nazionale Monza", "monza", 53, {"condition": "Dry", "rain_intensity_pct": 0, "wind_kph": 10, "ambient_temp_c": 26, "track_temp_c": 35, "phenomena": ["slipstream sensitive wind"]}),
    RaceSeed("Spanish Grand Prix", "Madrid Circuit", "madrid", 57, {"condition": "Hot Urban", "rain_intensity_pct": 4, "wind_kph": 12, "ambient_temp_c": 29, "track_temp_c": 42, "phenomena": ["urban heat island"]}),
    RaceSeed("Azerbaijan Grand Prix", "Baku City Circuit", "baku", 51, {"condition": "Windy", "rain_intensity_pct": 2, "wind_kph": 29, "ambient_temp_c": 24, "track_temp_c": 33, "phenomena": ["street-canyon crosswind"]}),
    RaceSeed("Singapore Grand Prix", "Marina Bay Street Circuit", "singapore", 62, {"condition": "Humid Night", "rain_intensity_pct": 18, "wind_kph": 8, "ambient_temp_c": 30, "track_temp_c": 37, "phenomena": ["humidity saturation"]}),
    RaceSeed("United States Grand Prix", "Circuit of the Americas", "cota", 56, {"condition": "Dry", "rain_intensity_pct": 6, "wind_kph": 20, "ambient_temp_c": 27, "track_temp_c": 39, "phenomena": ["elevation gusts"]}),
    RaceSeed("Mexico City Grand Prix", "Autodromo Hermanos Rodriguez", "mexico-city", 71, {"condition": "Thin Air", "rain_intensity_pct": 5, "wind_kph": 11, "ambient_temp_c": 22, "track_temp_c": 33, "phenomena": ["high altitude", "low air density"]}),
    RaceSeed("Sao Paulo Grand Prix", "Interlagos", "interlagos", 71, {"condition": "Storm Risk", "rain_intensity_pct": 28, "wind_kph": 15, "ambient_temp_c": 23, "track_temp_c": 29, "phenomena": ["pop-up storm cells"]}),
    RaceSeed("Las Vegas Grand Prix", "Las Vegas Strip Circuit", "las-vegas", 50, {"condition": "Cold Night", "rain_intensity_pct": 0, "wind_kph": 14, "ambient_temp_c": 14, "track_temp_c": 19, "phenomena": ["rapid tire cool-down"]}),
    RaceSeed("Qatar Grand Prix", "Lusail International Circuit", "lusail", 57, {"condition": "Hot Night", "rain_intensity_pct": 0, "wind_kph": 17, "ambient_temp_c": 29, "track_temp_c": 38, "phenomena": ["desert dust"]}),
    RaceSeed("Abu Dhabi Grand Prix", "Yas Marina Circuit", "yas-marina", 58, {"condition": "Warm Dusk", "rain_intensity_pct": 0, "wind_kph": 9, "ambient_temp_c": 27, "track_temp_c": 34, "phenomena": ["track temperature drop after sunset"]}),
]


SEGMENTS = [
    {"distance": 0.00, "speed": 84, "throttle": 62, "brake": 0, "gear": 3},
    {"distance": 0.08, "speed": 150, "throttle": 92, "brake": 0, "gear": 5},
    {"distance": 0.18, "speed": 228, "throttle": 100, "brake": 0, "gear": 7},
    {"distance": 0.31, "speed": 190, "throttle": 38, "brake": 64, "gear": 5},
    {"distance": 0.47, "speed": 162, "throttle": 46, "brake": 28, "gear": 4},
    {"distance": 0.61, "speed": 184, "throttle": 58, "brake": 12, "gear": 5},
    {"distance": 0.76, "speed": 238, "throttle": 95, "brake": 0, "gear": 7},
    {"distance": 0.88, "speed": 282, "throttle": 100, "brake": 0, "gear": 8},
    {"distance": 0.97, "speed": 296, "throttle": 92, "brake": 7, "gear": 8},
]


def request_json(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def request_get(path: str):
    with urllib.request.urlopen(f"{API_BASE}{path}") as response:
        return json.loads(response.read().decode("utf-8"))


def existing_session_names() -> set[str]:
    sessions = request_get("/sessions")
    return {session["name"] for session in sessions}


def sector_for_distance(distance: float) -> int:
    if distance < 0.333:
        return 1
    if distance < 0.666:
        return 2
    return 3


def coordinate(distance: float, lap_index: int) -> tuple[float, float]:
    angle = distance * 2 * math.pi
    radius_x = 0.62 + 0.08 * math.sin(angle * 3 + lap_index * 0.2)
    radius_y = 0.44 + 0.06 * math.cos(angle * 2 + lap_index * 0.14)
    x = 0.5 + math.cos(angle) * radius_x * 0.42
    y = 0.5 + math.sin(angle) * radius_y * 0.42
    return round(x, 4), round(y, 4)


def generate_points(seed: RaceSeed, session_id: str) -> list[dict]:
    rng = random.Random(seed.circuit_id)
    rain_factor = seed.weather["rain_intensity_pct"] / 100
    wind_factor = seed.weather["wind_kph"] / 100
    ambient = seed.weather["ambient_temp_c"]
    track_temp = seed.weather["track_temp_c"]

    points: list[dict] = []
    base_time = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    cumulative_energy = 0.0
    battery_pct = 100.0
    fuel_load = 110.0
    tire_temp = max(88.0, ambient + 11.0)
    engine_temp = max(96.0, ambient + 21.0)

    for lap in range(1, seed.laps + 1):
        lap_deg = (lap - 1) / max(seed.laps - 1, 1)
        lap_time_base_ms = int(82000 + lap_deg * 3200 + rain_factor * 9000 + wind_factor * 1500)
        sector_scale = [0.24, 0.39, 0.37]

        for index, segment in enumerate(SEGMENTS):
            lap_time_ms = int(lap_time_base_ms * segment["distance"])
            segment_noise = rng.uniform(-3.0, 3.0)
            speed_penalty = rain_factor * 42 + wind_factor * 18 + lap_deg * 11
            throttle_penalty = rain_factor * 18
            brake_bonus = rain_factor * 22 + wind_factor * 5

            speed_kph = max(72.0, segment["speed"] - speed_penalty + segment_noise)
            throttle_pct = max(24.0, min(100.0, segment["throttle"] - throttle_penalty + rng.uniform(-3.0, 3.0)))
            brake_pressure = max(0.0, min(120.0, segment["brake"] + brake_bonus + rng.uniform(-6.0, 6.0)))
            gear = max(2, min(8, segment["gear"]))
            rpm = int(max(10200, min(15450, 7600 + speed_kph * 28 + gear * 190 + rng.uniform(-150, 150))))

            battery_deployment = max(120.0, min(350.0, throttle_pct * 3.4 - brake_pressure * 0.6))
            cumulative_energy += battery_deployment * (lap_time_base_ms / POINTS_PER_LAP) / 1000
            battery_pct = max(18.0, battery_pct - 0.16 - rain_factor * 0.03 - lap_deg * 0.012)
            fuel_load = max(3.0, fuel_load - (0.16 + lap_deg * 0.02 + rain_factor * 0.01))
            tire_temp = max(72.0, tire_temp + 0.35 + track_temp * 0.005 + rain_factor * 0.05 - wind_factor * 0.12)
            engine_temp = max(88.0, engine_temp + 0.28 + ambient * 0.004 + wind_factor * 0.02)

            timestamp = base_time + timedelta(seconds=len(points) * 6)
            x, y = coordinate(segment["distance"], lap)

            points.append(
                {
                    "session_id": session_id,
                    "lap_number": lap,
                    "sector": sector_for_distance(segment["distance"]),
                    "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
                    "track_x": x,
                    "track_y": y,
                    "lap_distance_pct": round(segment["distance"], 4),
                    "speed_kph": round(speed_kph, 1),
                    "throttle_pct": round(throttle_pct, 1),
                    "brake_pressure_bar": round(brake_pressure, 1),
                    "rpm": rpm,
                    "gear": gear,
                    "lap_time_ms": lap_time_ms,
                    "tire_temp_c": round(tire_temp, 1),
                    "engine_temp_c": round(engine_temp, 1),
                    "battery_pct": round(battery_pct, 1),
                    "battery_deployment_kw": round(battery_deployment, 1),
                    "energy_used_kj": round(cumulative_energy, 1),
                    "fuel_load_kg": round(fuel_load, 1),
                }
            )

        base_time += timedelta(minutes=2)

    return points


def seed_race(seed: RaceSeed) -> str:
    session_name = f"2026 Race Weekend | {seed.event_name}"
    session = request_json(
        "/sessions/start",
        {
            "name": session_name,
            "track_name": seed.track_name,
            "total_laps": seed.laps,
            "mode": "replay",
            "configuration": {
                "circuit_id": seed.circuit_id,
                "weather": seed.weather,
                "source": "seeded-2026-calendar",
            },
        },
    )
    session_id = session["session_id"]
    points = generate_points(seed, session_id)
    request_json("/telemetry/ingest", {"session_id": session_id, "points": points})
    request_json(f"/sessions/{session_id}/stop", {"status": "completed"})
    return session_name


def main() -> None:
    names = existing_session_names()
    created = []
    skipped = []
    for race in RACES_2026:
      session_name = f"2026 Race Weekend | {race.event_name}"
      if session_name in names:
          skipped.append(session_name)
          continue
      created.append(seed_race(race))

    print(json.dumps({"created": created, "skipped": skipped}, indent=2))


if __name__ == "__main__":
    main()
