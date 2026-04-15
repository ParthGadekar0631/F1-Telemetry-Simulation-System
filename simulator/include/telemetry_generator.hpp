#pragma once

#include "types.hpp"

#include <string>
#include <vector>

namespace telemetry {

class TelemetryClient {
public:
    explicit TelemetryClient(std::string base_url);

    std::string start_session(const SimulationConfig& config, const std::string& mode);
    bool ingest_points(const std::string& session_id, const std::vector<TelemetryPoint>& points);
    bool stop_session(const std::string& session_id);

    static std::string escape(const std::string& value);

private:
    std::string post_json(const std::string& endpoint, const std::string& payload) const;
    static std::string extract_json_string(const std::string& body, const std::string& key);

    std::string base_url_;
};

}  // namespace telemetry
