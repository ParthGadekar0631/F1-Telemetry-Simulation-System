#pragma once

#include "telemetry_generator.hpp"
#include "types.hpp"

#include <string>
#include <vector>

namespace telemetry {

class ReplayEngine {
public:
    explicit ReplayEngine(double replay_speed);

    std::vector<TelemetryPoint> load_csv(const std::string& path) const;
    void replay_to_backend(const std::vector<TelemetryPoint>& points, TelemetryClient& client, const SimulationConfig& config) const;

private:
    double replay_speed_;
};

}  // namespace telemetry
