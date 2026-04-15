export type SessionSummary = {
  session_id: string;
  name: string;
  track_name: string;
  mode: string;
  status: string;
  total_laps: number;
  current_lap: number;
  best_lap_ms: number | null;
  average_lap_ms: number | null;
  total_alerts: number;
  total_anomalies: number;
  latest_timestamp: string | null;
};

export type TelemetryPoint = {
  id?: number;
  session_id: string;
  lap_number: number;
  sector: number;
  timestamp: string;
  track_x: number;
  track_y: number;
  lap_distance_pct: number;
  speed_kph: number;
  throttle_pct: number;
  brake_pressure_bar: number;
  rpm: number;
  gear: number;
  lap_time_ms: number;
  tire_temp_c: number;
  engine_temp_c: number;
  battery_pct: number;
  battery_deployment_kw: number;
  energy_used_kj: number;
  fuel_load_kg: number;
};

export type LiveTelemetryResponse = {
  session_id: string;
  is_live: boolean;
  latest: TelemetryPoint | null;
  updated_at: string | null;
};

export type Alert = {
  id: number;
  session_id: string;
  lap_number: number | null;
  timestamp: string;
  severity: string;
  category: string;
  message: string;
  metric_name: string;
  metric_value: number;
  threshold_value: number;
};

export type Anomaly = {
  id: number;
  session_id: string;
  lap_number: number | null;
  timestamp: string;
  anomaly_type: string;
  description: string;
  metric_name: string;
  metric_value: number;
  reference_value: number;
  magnitude: number;
};

export type LapSummary = {
  lap_number: number;
  lap_time_ms: number;
  sector_1_ms: number;
  sector_2_ms: number;
  sector_3_ms: number;
  average_speed_kph: number;
  top_speed_kph: number;
  fuel_burn_kg: number;
  energy_used_kj: number;
  avg_tire_temp_c: number;
  avg_engine_temp_c: number;
};

export type SessionAnalytics = {
  session_id: string;
  best_lap_number: number | null;
  best_lap_ms: number | null;
  average_lap_ms: number | null;
  peak_speed_kph: number | null;
  total_energy_used_kj: number;
  total_fuel_burn_kg: number;
  average_engine_temp_c: number | null;
  average_tire_temp_c: number | null;
  braking_zones_detected: number;
  lap_summaries: LapSummary[];
};

export type LapComparison = {
  lap_a: number;
  lap_b: number;
  lap_a_time_ms: number;
  lap_b_time_ms: number;
  lap_delta_ms: number;
  sector_deltas_ms: number[];
  fuel_delta_kg: number;
  energy_delta_kj: number;
  top_speed_delta_kph: number;
};

export type SectorComparison = {
  sector_number: number;
  lap_a_time_ms: number;
  lap_b_time_ms: number;
  delta_ms: number;
};

export type ReplayMetadata = {
  session_id: string;
  total_points: number;
  duration_ms: number;
  available_laps: number[];
  default_replay_speed: number;
};

export type ReplayResponse = {
  metadata: ReplayMetadata;
  points: TelemetryPoint[];
  started_at: string | null;
};
