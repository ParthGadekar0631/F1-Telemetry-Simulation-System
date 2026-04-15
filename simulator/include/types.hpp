#pragma once

#include <string>
#include <vector>

namespace telemetry {

struct SimulationConfig {
    std::string session_name {"Demo Race Run"};
    std::string track_name {"Silverstone"};
    double track_length_m {5891.0};
    int laps {5};
    int tick_rate_hz {10};
    double base_fuel_kg {100.0};
    double tire_wear_factor {1.0};
    double temperature_sensitivity {1.0};
    int telemetry_batch_size {10};
    std::string backend_url {"http://localhost:8000/api/v1"};
    int live_sleep_ms {100};
    double replay_speed {1.0};
};

struct TelemetryPoint {
    std::string session_id;
    int lap_number {1};
    int sector {1};
    std::string timestamp;
    double track_x {0.0};
    double track_y {0.0};
    double lap_distance_pct {0.0};
    double speed_kph {0.0};
    double throttle_pct {0.0};
    double brake_pressure_bar {0.0};
    int rpm {0};
    int gear {1};
    int lap_time_ms {0};
    double tire_temp_c {88.0};
    double engine_temp_c {96.0};
    double battery_pct {100.0};
    double battery_deployment_kw {0.0};
    double energy_used_kj {0.0};
    double fuel_load_kg {100.0};
};

struct TrackSegment {
    std::string name;
    double start_pct {0.0};
    double end_pct {0.0};
    double target_speed_kph {180.0};
    double braking_bias {0.0};
};

struct CarState {
    int lap_number {1};
    int sector {1};
    double elapsed_session_s {0.0};
    double elapsed_lap_s {0.0};
    double distance_on_lap_m {0.0};
    double speed_kph {95.0};
    double throttle_pct {42.0};
    double brake_pressure_bar {0.0};
    int rpm {10500};
    int gear {3};
    double tire_temp_c {88.0};
    double engine_temp_c {96.0};
    double battery_pct {100.0};
    double battery_deployment_kw {0.0};
    double energy_used_kj {0.0};
    double fuel_load_kg {100.0};
    std::vector<double> sector_times_ms {0.0, 0.0, 0.0};
    double sector_elapsed_s {0.0};
    bool session_complete {false};
};

std::string iso_timestamp_now();

}  // namespace telemetry
