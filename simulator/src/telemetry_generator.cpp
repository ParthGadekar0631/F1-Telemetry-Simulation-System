#include "telemetry_generator.hpp"

#include <curl/curl.h>

#include <regex>
#include <sstream>
#include <stdexcept>
#include <utility>

namespace telemetry {

namespace {

size_t write_callback(char* contents, size_t size, size_t nmemb, void* userp) {
    auto* buffer = static_cast<std::string*>(userp);
    buffer->append(contents, size * nmemb);
    return size * nmemb;
}

std::string point_to_json(const TelemetryPoint& point) {
    std::ostringstream stream;
    stream << "{"
           << "\"session_id\":\"" << TelemetryClient::escape(point.session_id) << "\","
           << "\"lap_number\":" << point.lap_number << ","
           << "\"sector\":" << point.sector << ","
           << "\"timestamp\":\"" << TelemetryClient::escape(point.timestamp) << "\","
           << "\"track_x\":" << point.track_x << ","
           << "\"track_y\":" << point.track_y << ","
           << "\"lap_distance_pct\":" << point.lap_distance_pct << ","
           << "\"speed_kph\":" << point.speed_kph << ","
           << "\"throttle_pct\":" << point.throttle_pct << ","
           << "\"brake_pressure_bar\":" << point.brake_pressure_bar << ","
           << "\"rpm\":" << point.rpm << ","
           << "\"gear\":" << point.gear << ","
           << "\"lap_time_ms\":" << point.lap_time_ms << ","
           << "\"tire_temp_c\":" << point.tire_temp_c << ","
           << "\"engine_temp_c\":" << point.engine_temp_c << ","
           << "\"battery_pct\":" << point.battery_pct << ","
           << "\"battery_deployment_kw\":" << point.battery_deployment_kw << ","
           << "\"energy_used_kj\":" << point.energy_used_kj << ","
           << "\"fuel_load_kg\":" << point.fuel_load_kg
           << "}";
    return stream.str();
}

}  // namespace

TelemetryClient::TelemetryClient(std::string base_url)
    : base_url_(std::move(base_url)) {
    curl_global_init(CURL_GLOBAL_DEFAULT);
}

std::string TelemetryClient::start_session(const SimulationConfig& config, const std::string& mode) {
    std::ostringstream payload;
    payload << "{"
            << "\"name\":\"" << escape(config.session_name) << "\","
            << "\"track_name\":\"" << escape(config.track_name) << "\","
            << "\"total_laps\":" << config.laps << ","
            << "\"mode\":\"" << escape(mode) << "\","
            << "\"configuration\":{"
            << "\"track_length_m\":" << config.track_length_m << ","
            << "\"tick_rate_hz\":" << config.tick_rate_hz << ","
            << "\"base_fuel_kg\":" << config.base_fuel_kg << ","
            << "\"tire_wear_factor\":" << config.tire_wear_factor << ","
            << "\"temperature_sensitivity\":" << config.temperature_sensitivity << ","
            << "\"replay_speed\":" << config.replay_speed
            << "}"
            << "}";

    const std::string body = post_json("/sessions/start", payload.str());
    const std::string session_id = extract_json_string(body, "session_id");
    if (session_id.empty()) {
        throw std::runtime_error("Unable to parse session_id from backend response");
    }
    return session_id;
}

bool TelemetryClient::ingest_points(const std::string& session_id, const std::vector<TelemetryPoint>& points) {
    std::ostringstream payload;
    payload << "{"
            << "\"session_id\":\"" << escape(session_id) << "\","
            << "\"points\":[";

    for (std::size_t index = 0; index < points.size(); ++index) {
        if (index > 0) {
            payload << ",";
        }
        payload << point_to_json(points[index]);
    }

    payload << "]}";
    post_json("/telemetry/ingest", payload.str());
    return true;
}

bool TelemetryClient::stop_session(const std::string& session_id) {
    post_json("/sessions/" + session_id + "/stop", "{\"status\":\"completed\"}");
    return true;
}

std::string TelemetryClient::post_json(const std::string& endpoint, const std::string& payload) const {
    CURL* curl = curl_easy_init();
    if (curl == nullptr) {
        throw std::runtime_error("Failed to initialize curl");
    }

    std::string response_body;
    curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");

    curl_easy_setopt(curl, CURLOPT_URL, (base_url_ + endpoint).c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_body);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10L);

    const CURLcode result = curl_easy_perform(curl);
    long status_code = 0;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &status_code);

    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);

    if (result != CURLE_OK || status_code >= 300) {
        throw std::runtime_error("Backend request failed at " + endpoint);
    }

    return response_body;
}

std::string TelemetryClient::escape(const std::string& value) {
    std::string escaped;
    escaped.reserve(value.size());

    for (const char character : value) {
        if (character == '\\') {
            escaped += "\\\\";
        } else if (character == '"') {
            escaped += "\\\"";
        } else {
            escaped += character;
        }
    }

    return escaped;
}

std::string TelemetryClient::extract_json_string(const std::string& body, const std::string& key) {
    const std::regex pattern("\"" + key + "\"\\s*:\\s*\"([^\"]+)\"");
    std::smatch matches;
    if (std::regex_search(body, matches, pattern) && matches.size() > 1) {
        return matches[1];
    }
    return {};
}

}  // namespace telemetry
