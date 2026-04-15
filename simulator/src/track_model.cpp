#include "track_model.hpp"

#include <cmath>
#include <utility>

namespace telemetry {

namespace {

constexpr double kPi = 3.14159265358979323846;

std::vector<TrackSegment> build_segments() {
    return {
        {"Main Straight", 0.00, 0.10, 332.0, 0.00},
        {"Turn 1", 0.10, 0.16, 124.0, 0.88},
        {"Acceleration 1", 0.16, 0.28, 278.0, 0.10},
        {"Lesmo Entry", 0.28, 0.36, 168.0, 0.55},
        {"Lesmo Exit", 0.36, 0.47, 236.0, 0.22},
        {"Back Straight", 0.47, 0.59, 316.0, 0.00},
        {"Ascari Entry", 0.59, 0.67, 158.0, 0.66},
        {"Ascari Exit", 0.67, 0.78, 250.0, 0.18},
        {"Parabolica", 0.78, 0.92, 214.0, 0.41},
        {"Front Straight", 0.92, 1.00, 325.0, 0.00},
    };
}

}  // namespace

TrackModel::TrackModel(double track_length_m, std::string track_name)
    : track_length_m_(track_length_m),
      track_name_(std::move(track_name)),
      segments_(build_segments()) {}

double TrackModel::length_m() const {
    return track_length_m_;
}

const std::string& TrackModel::name() const {
    return track_name_;
}

int TrackModel::sector_for_progress(double progress_pct) const {
    if (progress_pct < 0.333333) {
        return 1;
    }
    if (progress_pct < 0.666666) {
        return 2;
    }
    return 3;
}

double TrackModel::target_speed_for_progress(double progress_pct) const {
    for (const auto& segment : segments_) {
        if (progress_pct >= segment.start_pct && progress_pct < segment.end_pct) {
            return segment.target_speed_kph;
        }
    }
    return segments_.front().target_speed_kph;
}

std::pair<double, double> TrackModel::coordinate_for_progress(double progress_pct) const {
    const double theta = progress_pct * 2.0 * kPi;
    const double base_x = std::cos(theta) * 420.0;
    const double base_y = std::sin(theta) * 280.0;
    const double distortion = 1.0 + 0.16 * std::sin(3.0 * theta) - 0.08 * std::cos(2.0 * theta);
    const double x = base_x * distortion + 38.0 * std::sin(theta * 5.0);
    const double y = base_y * (1.0 - 0.05 * std::sin(theta * 4.0)) + 22.0 * std::cos(theta * 3.0);
    return {x, y};
}

const std::vector<TrackSegment>& TrackModel::segments() const {
    return segments_;
}

}  // namespace telemetry
