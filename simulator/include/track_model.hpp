#pragma once

#include "types.hpp"

#include <string>
#include <utility>
#include <vector>

namespace telemetry {

class TrackModel {
public:
    explicit TrackModel(double track_length_m, std::string track_name);

    double length_m() const;
    const std::string& name() const;
    int sector_for_progress(double progress_pct) const;
    double target_speed_for_progress(double progress_pct) const;
    std::pair<double, double> coordinate_for_progress(double progress_pct) const;
    const std::vector<TrackSegment>& segments() const;

private:
    double track_length_m_;
    std::string track_name_;
    std::vector<TrackSegment> segments_;
};

}  // namespace telemetry
