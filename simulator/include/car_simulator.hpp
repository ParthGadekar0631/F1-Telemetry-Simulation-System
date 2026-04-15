#pragma once

#include "track_model.hpp"
#include "types.hpp"

#include <optional>
#include <random>

namespace telemetry {

class CarSimulator {
public:
    CarSimulator(SimulationConfig config, TrackModel track);

    std::optional<TelemetryPoint> step();
    const CarState& state() const;
    bool finished() const;

private:
    void update_sector_state(double previous_progress, double current_progress);
    void update_powertrain(double dt_s, double target_speed_kph);
    void complete_lap_if_needed();

    SimulationConfig config_;
    TrackModel track_;
    CarState state_;
    std::mt19937 rng_;
};

}  // namespace telemetry
