# F1 Telemetry Simulation System

Production-style end-to-end telemetry platform for a simulated Formula 1 race car. The system combines a C++ vehicle simulator, a FastAPI analytics backend, PostgreSQL session storage, and a React + TypeScript engineering dashboard for live telemetry, lap replay, alerts, and comparative analysis.

## Why This Project Matters

Motorsport software is not just about plotting signals. A credible telemetry stack needs:

- deterministic signal generation from an internally consistent vehicle model
- time-series ingestion and storage with replayable session history
- lap, sector, and run-level analytics for engineering decisions
- alerting and anomaly detection for operational awareness
- a UI that supports both live monitoring and post-run review

This project is built to demonstrate that end-to-end workflow in a resume-ready format.

## Architecture Overview

```text
                    +------------------------------------+
                    |      C++ Simulation Core           |
                    |------------------------------------|
                    | Track model                        |
                    | Vehicle state update loop          |
                    | Sector/lap timing                  |
                    | Live HTTP telemetry streaming      |
                    | Replay from exported CSV           |
                    +------------------+-----------------+
                                       |
                                       | HTTP / JSON
                                       v
                    +------------------------------------+
                    |      FastAPI Telemetry Backend     |
                    |------------------------------------|
                    | Session lifecycle                  |
                    | Telemetry ingestion                |
                    | Lap + sector summarization         |
                    | Alerts + anomaly detection         |
                    | Replay metadata + export services  |
                    | Comparison + analytics APIs        |
                    +------------------+-----------------+
                                       |
                 +---------------------+----------------------+
                 |                                            |
                 v                                            v
     +---------------------------+              +---------------------------+
     |      PostgreSQL           |              | React + TypeScript UI     |
     |---------------------------|              |---------------------------|
     | telemetry_sessions        |              | Live telemetry cards      |
     | telemetry_points          |              | Telemetry charts          |
     | lap_summaries             |              | Track map                 |
     | sector_summaries          |              | Replay controls           |
     | telemetry_alerts          |              | Session history           |
     | anomaly_events            |              | Lap delta + alerts        |
     | replay_metadata           |              | CSV / JSON export links   |
     | export_history            |              +---------------------------+
     +---------------------------+
```

## Tech Stack

- Simulator: C++20, CMake, libcurl
- Backend: Python, FastAPI, SQLAlchemy, Pydantic, PostgreSQL
- Frontend: React 19, TypeScript, Vite, Recharts
- Infra: Docker Compose, Makefile
- Testing: pytest, native C++ test binary via CTest

## Project Structure

```text
F1-Telemetry-Simulation-System/
├── README.md
├── Makefile
├── docker-compose.yml
├── docs/
│   └── screenshots/
├── simulator/
│   ├── CMakeLists.txt
│   ├── Dockerfile
│   ├── config/
│   │   └── default.ini
│   ├── include/
│   │   ├── car_simulator.hpp
│   │   ├── replay_engine.hpp
│   │   ├── telemetry_generator.hpp
│   │   ├── track_model.hpp
│   │   ├── types.hpp
│   │   └── utils.hpp
│   ├── src/
│   │   ├── car_simulator.cpp
│   │   ├── main.cpp
│   │   ├── replay_engine.cpp
│   │   ├── telemetry_generator.cpp
│   │   ├── track_model.cpp
│   │   └── utils.cpp
│   └── tests/
│       └── simulator_tests.cpp
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── api/routes/
│       ├── core/
│       ├── db/
│       ├── models/
│       ├── schemas/
│       ├── services/
│       │   ├── alerts/
│       │   ├── analytics/
│       │   ├── exports/
│       │   ├── ingestion/
│       │   └── replay/
│       └── tests/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── components/
│       ├── hooks/
│       ├── pages/
│       ├── services/
│       ├── styles/
│       ├── types/
│       └── utils/
└── sample_data/
    └── demo_sessions/
```

## System Design

### C++ Simulation Core

The simulator models a single F1-style car running multi-lap sessions on a segmented track. Each simulation tick updates:

- target speed by track segment
- throttle and brake state based on target-speed error
- RPM and gear selection
- tire and engine temperature drift
- fuel burn and ERS depletion
- sector assignment and lap progression
- track coordinates for map rendering

The simulator supports:

- `live` mode: starts a backend session, streams telemetry in configurable batches, and closes the session
- `replay` mode: reads a previously exported CSV session and re-streams it to the backend

### FastAPI Backend

The backend is organized around clear service boundaries:

- `ingestion`: validates incoming points, persists telemetry, updates session state, and refreshes replay metadata
- `alerts`: rule-based threshold alerts and anomaly events
- `analytics`: lap summaries, sector summaries, best lap, braking-zone counts, energy/fuel consumption, and lap comparison
- `replay`: serves lap-scoped historical points for playback
- `exports`: CSV and JSON export generation with history tracking

### React Dashboard

The frontend is a single-page engineering dashboard with:

- live metric cards for speed, RPM, gear, fuel, battery, and best lap
- synchronized time-series charts for selected telemetry signals
- a 2D SVG track map with current or replay cursor
- lap replay controls with speed and scrubber
- session history and session analytics
- lap delta comparison and sector delta display
- alerts and anomaly panel
- export links for CSV and JSON

## Database Schema Summary

The PostgreSQL model includes:

- `telemetry_sessions`: session metadata, lifecycle, configuration
- `telemetry_points`: raw signal samples for every tick
- `lap_summaries`: lap-level aggregates and totals
- `sector_summaries`: per-sector timing and entry/exit behavior
- `telemetry_alerts`: threshold-based operational warnings
- `anomaly_events`: suspicious telemetry behavior beyond simple thresholds
- `replay_metadata`: replay availability and timing metadata
- `export_history`: audit trail for CSV and JSON exports

## Live Mode vs Replay Mode

### Live Mode

- simulator creates a session with `/api/v1/sessions/start`
- simulator emits telemetry batches to `/api/v1/telemetry/ingest`
- frontend polls live and analytics endpoints
- backend updates alerts, anomalies, and lap summaries as data arrives

### Replay Mode

- simulator or backend uses previously stored/exported session data
- frontend requests replay metadata and lap-specific points
- user scrubs or plays the lap timeline
- charts and track map move with replay state

## Alert and Anomaly Logic

Current rule-based detection includes:

- engine overheating
- tire temperature warnings
- low-fuel warnings
- excessive brake pressure events
- sudden speed drops without proportional braking
- abnormal battery state-of-charge drops
- sharp engine temperature spikes

The detection is intentionally structured so a more advanced statistical or ML model can be added later without changing the API surface.

## Setup Instructions

## 1. Docker Setup

Prerequisites:

- Docker Desktop
- Make or direct `docker compose`

Run:

```bash
docker compose up --build
```

Services:

- frontend: [http://localhost:5173](http://localhost:5173)
- backend API: [http://localhost:8000/docs](http://localhost:8000/docs)
- PostgreSQL: `localhost:5432`

## 2. Local Non-Docker Setup

### Backend

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Set `DATABASE_URL` if your PostgreSQL instance differs from the default:

```bash
export DATABASE_URL=postgresql+psycopg2://telemetry:telemetry@localhost:5432/telemetry
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

### Simulator

Prerequisites:

- CMake
- C++20 compiler
- libcurl development package

```bash
cmake -S simulator -B simulator/build
cmake --build simulator/build
```

## Running the Simulator

### Live Streaming

```bash
simulator/build/f1_telemetry_simulator --config simulator/config/default.ini --mode live
```

### Replay a Recorded Session

```bash
simulator/build/f1_telemetry_simulator \
  --config simulator/config/default.ini \
  --mode replay \
  --replay-file sample_data/demo_sessions/demo_session.csv
```

## Makefile Shortcuts

```bash
make up
make down
make backend-test
make simulator-build
make simulator-test
make simulator-live
make simulator-replay
```

## Example API Usage

### Start a Session

```bash
curl -X POST http://localhost:8000/api/v1/sessions/start \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monza Long Run",
    "track_name": "Autodromo Nazionale Monza",
    "total_laps": 6,
    "mode": "live",
    "configuration": {
      "track_length_m": 5793,
      "tick_rate_hz": 10,
      "base_fuel_kg": 96,
      "replay_speed": 2.0
    }
  }'
```

### Ingest Telemetry

```bash
curl -X POST http://localhost:8000/api/v1/telemetry/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "replace-with-session-id",
    "points": [
      {
        "session_id": "replace-with-session-id",
        "lap_number": 1,
        "sector": 1,
        "timestamp": "2026-04-14T19:00:00Z",
        "track_x": 0.0,
        "track_y": 0.52,
        "lap_distance_pct": 0.10,
        "speed_kph": 160.0,
        "throttle_pct": 82.0,
        "brake_pressure_bar": 4.0,
        "rpm": 12800,
        "gear": 5,
        "lap_time_ms": 10000,
        "tire_temp_c": 94.0,
        "engine_temp_c": 103.0,
        "battery_pct": 72.0,
        "battery_deployment_kw": 280.0,
        "energy_used_kj": 30.0,
        "fuel_load_kg": 78.0
      }
    ]
  }'
```

### Inspect Analytics

```bash
curl http://localhost:8000/api/v1/analytics/sessions/<session_id>/summary
curl http://localhost:8000/api/v1/analytics/sessions/<session_id>/laps/compare?lap_a=1&lap_b=2
curl http://localhost:8000/api/v1/replay/<session_id>/laps/1
```

## Demo Workflow

1. Start PostgreSQL, backend, and frontend with Docker Compose.
2. Run the C++ simulator in live mode.
3. Open the dashboard and watch live cards, charts, and the track map update.
4. Stop the session and inspect generated lap summaries.
5. Use replay controls to scrub a prior lap.
6. Compare two laps and inspect sector delta.
7. Trigger exports for CSV or JSON.

## Tests

### Backend

```bash
cd backend
pytest
```

### Simulator

```bash
ctest --test-dir simulator/build --output-on-failure
```

## Dashboard Screenshots

### Main Telemetry Dashboard

Overview of the race engineering workspace with live metrics, telemetry traces, track map, replay controls, and session analysis panels.

![Main telemetry dashboard](docs/screenshots/dashboard.png)

### Telemetry Signal Analysis

Signal view showing time-series behavior for speed, RPM, throttle, braking, thermal state, and energy or fuel trends across the session.

![Telemetry signal analysis](docs/screenshots/graph.png)

### Alerting and Operational Monitoring

Alert panel highlighting thermal, braking, fuel, or anomaly conditions that require engineering review during a run or replay.

![Alert and anomaly monitoring](docs/screenshots/alert.png)

### Session History and Review

Historical session browser for selecting prior runs, replaying laps, and comparing completed telemetry sessions stored in PostgreSQL.

![Session history and replay review](docs/screenshots/history.png)

## Future Improvements

- multi-car telemetry sessions and comparative overlays
- WebSocket live streaming instead of polling
- driver-in-the-loop input model
- tire degradation and grip-loss modeling
- richer replay timeline indexing and event bookmarks
- Prometheus/Grafana observability for system metrics
- model-based anomaly scoring beyond rule thresholds

## Verification Notes

The repository currently includes:

- complete backend syntax validation via `python -m compileall backend/app`
- backend pytest suites for session flow, alerts, analytics, replay, and exports
- simulator native tests defined in CTest

In the current local shell:

- Python and Node are available
- CMake is not installed, so simulator compilation was not executed here
- Python backend dependencies were not preinstalled, so pytest execution was not completed in this shell
