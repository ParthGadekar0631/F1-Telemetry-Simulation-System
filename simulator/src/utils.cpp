#include "utils.hpp"

#include <chrono>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <stdexcept>

namespace telemetry {

std::string iso_timestamp_now() {
    const auto now = std::chrono::system_clock::now();
    const std::time_t now_c = std::chrono::system_clock::to_time_t(now);
    std::tm utc_time {};
#if defined(_WIN32)
    gmtime_s(&utc_time, &now_c);
#else
    gmtime_r(&now_c, &utc_time);
#endif
    std::ostringstream stream;
    stream << std::put_time(&utc_time, "%Y-%m-%dT%H:%M:%SZ");
    return stream.str();
}

SimulationConfig load_config(const std::string& path) {
    const auto values = parse_key_value_file(path);
    SimulationConfig config;

    if (values.contains("session_name")) {
        config.session_name = values.at("session_name");
    }
    if (values.contains("track_name")) {
        config.track_name = values.at("track_name");
    }
    if (values.contains("track_length_m")) {
        config.track_length_m = std::stod(values.at("track_length_m"));
    }
    if (values.contains("laps")) {
        config.laps = std::stoi(values.at("laps"));
    }
    if (values.contains("tick_rate_hz")) {
        config.tick_rate_hz = std::stoi(values.at("tick_rate_hz"));
    }
    if (values.contains("base_fuel_kg")) {
        config.base_fuel_kg = std::stod(values.at("base_fuel_kg"));
    }
    if (values.contains("tire_wear_factor")) {
        config.tire_wear_factor = std::stod(values.at("tire_wear_factor"));
    }
    if (values.contains("temperature_sensitivity")) {
        config.temperature_sensitivity = std::stod(values.at("temperature_sensitivity"));
    }
    if (values.contains("telemetry_batch_size")) {
        config.telemetry_batch_size = std::stoi(values.at("telemetry_batch_size"));
    }
    if (values.contains("backend_url")) {
        config.backend_url = values.at("backend_url");
    }
    if (values.contains("live_sleep_ms")) {
        config.live_sleep_ms = std::stoi(values.at("live_sleep_ms"));
    }
    if (values.contains("replay_speed")) {
        config.replay_speed = std::stod(values.at("replay_speed"));
    }

    return config;
}

std::map<std::string, std::string> parse_key_value_file(const std::string& path) {
    std::ifstream stream(path);
    if (!stream.good()) {
        throw std::runtime_error("Unable to read config file: " + path);
    }

    std::map<std::string, std::string> values;
    std::string line;
    while (std::getline(stream, line)) {
        const std::string trimmed = trim(line);
        if (trimmed.empty() || trimmed.starts_with('#')) {
            continue;
        }

        const auto separator = trimmed.find('=');
        if (separator == std::string::npos) {
            continue;
        }

        values[trim(trimmed.substr(0, separator))] = trim(trimmed.substr(separator + 1));
    }

    return values;
}

std::vector<std::string> split(const std::string& value, char delimiter) {
    std::vector<std::string> parts;
    std::stringstream stream(value);
    std::string part;
    while (std::getline(stream, part, delimiter)) {
        parts.push_back(part);
    }
    return parts;
}

double clamp(double value, double low, double high) {
    if (value < low) {
        return low;
    }
    if (value > high) {
        return high;
    }
    return value;
}

std::string trim(const std::string& value) {
    const auto start = value.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) {
        return {};
    }
    const auto end = value.find_last_not_of(" \t\r\n");
    return value.substr(start, end - start + 1);
}

}  // namespace telemetry
