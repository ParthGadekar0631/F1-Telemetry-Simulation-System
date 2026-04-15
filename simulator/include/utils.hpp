#pragma once

#include "types.hpp"

#include <map>
#include <string>
#include <vector>

namespace telemetry {

SimulationConfig load_config(const std::string& path);
std::map<std::string, std::string> parse_key_value_file(const std::string& path);
std::vector<std::string> split(const std::string& value, char delimiter);
double clamp(double value, double low, double high);
std::string trim(const std::string& value);

}  // namespace telemetry
