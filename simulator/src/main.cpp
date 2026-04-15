#include "car_simulator.hpp"
#include "replay_engine.hpp"
#include "telemetry_generator.hpp"
#include "utils.hpp"

#include <chrono>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

namespace telemetry {

struct CliArgs {
    std::string config_path {"config/default.ini"};
    std::string mode {"live"};
    std::string replay_file;
};

CliArgs parse_args(int argc, char** argv) {
    CliArgs args;

    for (int index = 1; index < argc; ++index) {
        std::string current = argv[index];
        if (current == "--config" && index + 1 < argc) {
            args.config_path = argv[++index];
        } else if (current == "--mode" && index + 1 < argc) {
            args.mode = argv[++index];
        } else if (current == "--replay-file" && index + 1 < argc) {
            args.replay_file = argv[++index];
        }
    }

    return args;
}

int run_live(const SimulationConfig& config) {
    TrackModel track(config.track_length_m, config.track_name);
    CarSimulator simulator(config, track);
    TelemetryClient client(config.backend_url);

    const std::string session_id = client.start_session(config, "live");
    std::vector<TelemetryPoint> batch;
    batch.reserve(static_cast<std::size_t>(config.telemetry_batch_size));

    while (!simulator.finished()) {
        auto point = simulator.step();
        if (!point.has_value()) {
            break;
        }

        point->session_id = session_id;
        batch.push_back(*point);

        if (batch.size() >= static_cast<std::size_t>(config.telemetry_batch_size)) {
            client.ingest_points(session_id, batch);
            batch.clear();
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(config.live_sleep_ms));
    }

    if (!batch.empty()) {
        client.ingest_points(session_id, batch);
    }

    client.stop_session(session_id);
    std::cout << "Completed live session " << session_id << "\n";
    return 0;
}

int run_replay(const SimulationConfig& config, const std::string& replay_file) {
    if (replay_file.empty()) {
        throw std::runtime_error("Replay mode requires --replay-file");
    }

    TelemetryClient client(config.backend_url);
    ReplayEngine replay(config.replay_speed);
    const auto points = replay.load_csv(replay_file);
    replay.replay_to_backend(points, client, config);
    std::cout << "Replayed " << points.size() << " telemetry points from " << replay_file << "\n";
    return 0;
}

}  // namespace telemetry

int main(int argc, char** argv) {
    try {
        const auto args = telemetry::parse_args(argc, argv);
        const auto config = telemetry::load_config(args.config_path);

        if (args.mode == "replay") {
            return telemetry::run_replay(config, args.replay_file);
        }

        return telemetry::run_live(config);
    } catch (const std::exception& error) {
        std::cerr << "Simulator error: " << error.what() << "\n";
        return 1;
    }
}
