import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { TelemetryPoint } from "../types/api";


const SIGNALS: Record<string, { label: string; color: string }> = {
  speed_kph: { label: "Speed", color: "#d62939" },
  rpm: { label: "RPM", color: "#18212f" },
  throttle_pct: { label: "Throttle", color: "#ff9f1c" },
  brake_pressure_bar: { label: "Brake", color: "#457b9d" },
  engine_temp_c: { label: "Engine Temp", color: "#9f2b68" },
  tire_temp_c: { label: "Tire Temp", color: "#7a9e7e" },
  battery_pct: { label: "Battery", color: "#1d6f42" },
  fuel_load_kg: { label: "Fuel", color: "#7d5a50" },
};

type SignalChartProps = {
  points: TelemetryPoint[];
  selectedSignals: string[];
  onToggleSignal: (signal: string) => void;
};


export function SignalChart({ points, selectedSignals, onToggleSignal }: SignalChartProps) {
  return (
    <section className="panel">
      <div className="panel-header split">
        <div>
          <p className="eyebrow">Time-series signals</p>
          <h3>Telemetry Trace</h3>
        </div>
        <div className="signal-toggle-group">
          {Object.entries(SIGNALS).map(([key, signal]) => (
            <button
              key={key}
              type="button"
              className={`signal-chip ${selectedSignals.includes(key) ? "active" : ""}`}
              onClick={() => onToggleSignal(key)}
            >
              {signal.label}
            </button>
          ))}
        </div>
      </div>
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={points}>
            <CartesianGrid strokeDasharray="2 6" stroke="#d9d4cc" />
            <XAxis dataKey="lap_time_ms" stroke="#555" tickFormatter={(value) => `${Math.round(value / 1000)}s`} />
            <YAxis stroke="#555" />
            <Tooltip />
            <Legend />
            {selectedSignals.map((signal) => (
              <Line
                key={signal}
                type="monotone"
                dataKey={signal}
                stroke={SIGNALS[signal]?.color ?? "#000"}
                strokeWidth={2.3}
                dot={false}
                name={SIGNALS[signal]?.label ?? signal}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
