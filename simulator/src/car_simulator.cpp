#include "car_simulator.hpp"

#include "utils.hpp"

#include <utility>

namespace telemetry {

namespace {

int gear_for_speed(double speed_kph) {
    if (speed_kph < 70.0) {
        return 2;
    }
    if (speed_kph < 110.0) {
        return 3;
    }
    if (speed_kph < 150.0) {
        return 4;
    }
    if (speed_kph < 195.0) {
        return 5;
    }
    if (speed_kph < 240.0) {
        return 6;
    }
    if (speed_kph < 285.0) {
        return 7;
    }
    return 8;
}

}  // namespace

CarSimulator::CarSimulator(SimulationConfig config, TrackModel track)
    : config_(std::move(config)),
      track_(std::move(track)),
      rng_(42) {
    state_.fuel_load_kg = config_.base_fuel_kg;
    state_.battery_pct = 100.0;
    state_.tire_temp_c = 88.0;
    state_.engine_temp_c = 96.0;
}

std::optional<TelemetryPoint> CarSimulator::step() {
    if (state_.session_complete) {
        return std::nullopt;
    }

    const double dt_s = 1.0 / static_cast<double>(config_.tick_rate_hz);
    const double previous_progress = state_.distance_on_lap_m / track_.length_m();
    const double target_speed_kph = track_.target_speed_for_progress(previous_progress);

    update_powertrain(dt_s, target_speed_kph);

    const double speed_m_s = state_.speed_kph / 3.6;
    state_.distance_on_lap_m += speed_m_s * dt_s;
    state_.elapsed_lap_s += dt_s;
    state_.elapsed_session_s += dt_s;
    state_.sector_elapsed_s += dt_s;

    complete_lap_if_needed();

    const double progress = clamp(state_.distance_on_lap_m / track_.length_m(), 0.0, 0.9999);
    update_sector_state(previous_progress, progress);

    const auto [track_x, track_y] = track_.coordinate_for_progress(progress);
    TelemetryPoint point;
    point.lap_number = state_.lap_number;
    point.sector = state_.sector;
    point.timestamp = iso_timestamp_now();
    point.track_x = track_x;
    point.track_y = track_y;
    point.lap_distance_pct = progress;
    point.speed_kph = state_.speed_kph;
    point.throttle_pct = state_.throttle_pct;
    point.brake_pressure_bar = state_.brake_pressure_bar;
    point.rpm = state_.rpm;
    point.gear = state_.gear;
    point.lap_time_ms = static_cast<int>(state_.elapsed_lap_s * 1000.0);
    point.tire_temp_c = state_.tire_temp_c;
    point.engine_temp_c = state_.engine_temp_c;
    point.battery_pct = state_.battery_pct;
    point.battery_deployment_kw = state_.battery_deployment_kw;
    point.energy_used_kj = state_.energy_used_kj;
    point.fuel_load_kg = state_.fuel_load_kg;
    return point;
}

const CarState& CarSimulator::state() const {
    return state_;
}

bool CarSimulator::finished() const {
    return state_.session_complete;
}

void CarSimulator::update_sector_state(double previous_progress, double current_progress) {
    const int previous_sector = track_.sector_for_progress(previous_progress);
    const int current_sector = track_.sector_for_progress(current_progress);

    if (current_sector != previous_sector && current_sector > previous_sector) {
        state_.sector_times_ms[previous_sector - 1] = state_.sector_elapsed_s * 1000.0;
        state_.sector_elapsed_s = 0.0;
    }

    state_.sector = current_sector;
}

void CarSimulator::update_powertrain(double dt_s, double target_speed_kph) {
    const double speed_delta = target_speed_kph - state_.speed_kph;
    const double aggression = clamp(speed_delta / 75.0, -1.0, 1.0);

    if (speed_delta > 4.0) {
        state_.throttle_pct = clamp(58.0 + aggression * 42.0, 0.0, 100.0);
        state_.brake_pressure_bar = 0.0;
    } else if (speed_delta < -6.0) {
        state_.throttle_pct = clamp(18.0 + aggression * 12.0, 0.0, 100.0);
        state_.brake_pressure_bar = clamp(-speed_delta * 0.9, 0.0, 120.0);
    } else {
        state_.throttle_pct = clamp(36.0 + aggression * 16.0, 0.0, 100.0);
        state_.brake_pressure_bar = 0.0;
    }

    const double throttle_force = (state_.throttle_pct / 100.0) * 11.0;
    const double braking_force = (state_.brake_pressure_bar / 120.0) * 16.0;
    const double drag_force = 0.00155 * state_.speed_kph * state_.speed_kph / 100.0;
    const double acceleration_m_s2 = throttle_force - braking_force - drag_force;
    const double next_speed_m_s = clamp(state_.speed_kph / 3.6 + acceleration_m_s2 * dt_s, 18.0, 92.0);
    state_.speed_kph = next_speed_m_s * 3.6;
    state_.gear = gear_for_speed(state_.speed_kph);
    state_.rpm = static_cast<int>(clamp(7800.0 + state_.speed_kph * 28.0 + state_.gear * 180.0, 7000.0, 15500.0));

    const double thermal_gain = (state_.throttle_pct / 100.0) * 1.4 + (state_.brake_pressure_bar / 120.0) * 0.9;
    const double cooling = clamp(state_.speed_kph / 330.0, 0.12, 0.9);
    state_.tire_temp_c += (thermal_gain * config_.temperature_sensitivity * config_.tire_wear_factor - cooling * 0.45) * dt_s;
    state_.engine_temp_c += ((state_.throttle_pct / 100.0) * 1.9 * config_.temperature_sensitivity - cooling * 0.38) * dt_s;

    state_.battery_deployment_kw = clamp((state_.throttle_pct / 100.0) * 350.0 - (state_.brake_pressure_bar / 120.0) * 80.0, -25.0, 350.0);
    const double battery_drain = (clamp(state_.battery_deployment_kw, 0.0, 350.0) / 350.0) * 0.42 * dt_s;
    const double battery_regen = (state_.brake_pressure_bar / 120.0) * 0.18 * dt_s;
    state_.battery_pct = clamp(state_.battery_pct - battery_drain + battery_regen, 12.0, 100.0);
    state_.energy_used_kj += clamp(state_.battery_deployment_kw, 0.0, 350.0) * dt_s;
    state_.fuel_load_kg = clamp(state_.fuel_load_kg - (0.015 + (state_.throttle_pct / 100.0) * 0.021) * dt_s, 0.8, config_.base_fuel_kg);
}

void CarSimulator::complete_lap_if_needed() {
    if (state_.distance_on_lap_m < track_.length_m()) {
        return;
    }

    state_.sector_times_ms[2] = state_.sector_elapsed_s * 1000.0;
    if (state_.lap_number >= config_.laps) {
        state_.distance_on_lap_m = track_.length_m() - 1.0;
        state_.session_complete = true;
        return;
    }

    state_.distance_on_lap_m -= track_.length_m();
    state_.elapsed_lap_s = 0.0;
    state_.sector_elapsed_s = 0.0;
    state_.sector = 1;
    state_.lap_number += 1;
}

}  // namespace telemetry
