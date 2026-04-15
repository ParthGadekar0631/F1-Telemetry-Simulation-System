#include "replay_engine.hpp"

#include "utils.hpp"

#include <chrono>
#include <fstream>
#include <stdexcept>
#include <thread>

namespace telemetry {

ReplayEngine::ReplayEngine(double replay_speed)
    : replay_speed_(replay_speed <= 0.0 ? 1.0 : replay_speed) {}

std::vector<TelemetryPoint> ReplayEngine::load_csv(const std::string& path) const {
    std::ifstream stream(path);
    if (!stream.good()) {
        throw std::runtime_error("Unable to open replay file: " + path);
    }

    std::string line;
    std::getline(stream, line);

    std::vector<TelemetryPoint> points;
    while (std::getline(stream, line)) {
        if (line.empty()) {
            continue;
        }

        const auto parts = split(line, ',');
        if (parts.size() < 18) {
            continue;
        }

        TelemetryPoint point;
        point.timestamp = parts[0];
        point.lap_number = std::stoi(parts[1]);
        point.sector = std::stoi(parts[2]);
        point.track_x = std::stod(parts[3]);
        point.track_y = std::stod(parts[4]);
        point.speed_kph = std::stod(parts[5]);
        point.throttle_pct = std::stod(parts[6]);
        point.brake_pressure_bar = std::stod(parts[7]);
        point.rpm = std::stoi(parts[8]);
        point.gear = std::stoi(parts[9]);
        point.lap_time_ms = std::stoi(parts[10]);
        point.tire_temp_c = std::stod(parts[11]);
        point.engine_temp_c = std::stod(parts[12]);
        point.battery_pct = std::stod(parts[13]);
        point.battery_deployment_kw = std::stod(parts[14]);
        point.energy_used_kj = std::stod(parts[15]);
        point.fuel_load_kg = std::stod(parts[16]);
        point.lap_distance_pct = std::stod(parts[17]);
        points.push_back(point);
    }

    return points;
}

void ReplayEngine::replay_to_backend(const std::vector<TelemetryPoint>& points, TelemetryClient& client, const SimulationConfig& config) const {
    if (points.empty()) {
        return;
    }

    const std::string session_id = client.start_session(config, "replay");
    for (auto point : points) {
        point.session_id = session_id;
        client.ingest_points(session_id, {point});
        std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<int>(100.0 / replay_speed_)));
    }
    client.stop_session(session_id);
}

}  // namespace telemetry
