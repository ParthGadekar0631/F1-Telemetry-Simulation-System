#include "car_simulator.hpp"
#include "track_model.hpp"

#include <cmath>
#include <cstdlib>
#include <iostream>

namespace {

void require(bool condition, const char* message) {
    if (!condition) {
        std::cerr << "Test failure: " << message << "\n";
        std::exit(1);
    }
}

}  // namespace

int main() {
    {
        telemetry::TrackModel track(5793.0, "Monza");
        const auto [x, y] = track.coordinate_for_progress(0.25);
        require(std::abs(x) < 600.0, "track x coordinate should stay bounded");
        require(std::abs(y) < 400.0, "track y coordinate should stay bounded");
        require(track.sector_for_progress(0.20) == 1, "first third should be sector one");
        require(track.sector_for_progress(0.50) == 2, "middle third should be sector two");
    }

    {
        telemetry::SimulationConfig config;
        config.laps = 2;
        config.tick_rate_hz = 20;
        config.base_fuel_kg = 96.0;

        telemetry::CarSimulator simulator(config, telemetry::TrackModel(config.track_length_m, config.track_name));
        const double initial_fuel = config.base_fuel_kg;
        int samples = 0;

        while (!simulator.finished() && samples < 5000) {
            const auto point = simulator.step();
            require(point.has_value(), "simulator should emit telemetry while active");
            require(point->speed_kph > 10.0, "speed should remain positive");
            require(point->gear >= 2 && point->gear <= 8, "gear should remain in a valid range");
            ++samples;
        }

        require(simulator.state().fuel_load_kg < initial_fuel, "fuel should burn down");
        require(simulator.finished(), "simulator should finish the configured number of laps");
    }

    std::cout << "simulator tests passed\n";
    return 0;
}
