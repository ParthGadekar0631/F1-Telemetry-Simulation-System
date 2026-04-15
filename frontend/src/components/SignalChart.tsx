import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  TooltipProps,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { NameType, ValueType } from "recharts/types/component/DefaultTooltipContent";

import type { TelemetryPoint } from "../types/api";


const SIGNALS: Record<string, { label: string; color: string; unit: string }> = {
  speed_kph: { label: "Speed", color: "#d62939", unit: "kph" },
  rpm: { label: "RPM", color: "#18212f", unit: "rpm" },
  throttle_pct: { label: "Throttle", color: "#ff9f1c", unit: "%" },
  brake_pressure_bar: { label: "Brake", color: "#457b9d", unit: "bar" },
  engine_temp_c: { label: "Engine Temp", color: "#9f2b68", unit: "C" },
  tire_temp_c: { label: "Tire Temp", color: "#7a9e7e", unit: "C" },
  battery_pct: { label: "Battery", color: "#1d6f42", unit: "%" },
  fuel_load_kg: { label: "Fuel", color: "#7d5a50", unit: "kg" },
};

export type ChartScaleMode = "relative" | "raw";
export type ChartScopeMode = "lap" | "all";

type SignalChartProps = {
  points: TelemetryPoint[];
  selectedSignals: string[];
  onToggleSignal: (signal: string) => void;
  scaleMode: ChartScaleMode;
  onScaleModeChange: (mode: ChartScaleMode) => void;
  scopeMode: ChartScopeMode;
  onScopeModeChange: (mode: ChartScopeMode) => void;
};


function formatSignalValue(signal: string, point: TelemetryPoint) {
  const value = point[signal as keyof TelemetryPoint];
  if (typeof value !== "number") {
    return "--";
  }

  const digits = signal === "rpm" ? 0 : 1;
  return `${value.toFixed(digits)} ${SIGNALS[signal]?.unit ?? ""}`.trim();
}

function ChartTooltip({ active, payload, label }: TooltipProps<ValueType, NameType>) {
  if (!active || !payload || payload.length === 0) {
    return null;
  }

  const point = payload[0].payload as TelemetryPoint;
  return (
    <div className="chart-tooltip">
      <strong>{`T+ ${Math.round(Number(label) / 1000)}s · Lap ${point.lap_number}`}</strong>
      {payload.map((item) => {
        const signal = String(item.dataKey);
        return (
          <div key={signal} className="chart-tooltip-row">
            <span style={{ color: item.color ?? "#000" }}>{SIGNALS[signal]?.label ?? signal}</span>
            <strong>{formatSignalValue(signal, point)}</strong>
          </div>
        );
      })}
    </div>
  );
}

export function SignalChart({
  points,
  selectedSignals,
  onToggleSignal,
  scaleMode,
  onScaleModeChange,
  scopeMode,
  onScopeModeChange,
}: SignalChartProps) {
  const firstTimestamp = points.length > 0 ? new Date(points[0].timestamp).getTime() : 0;
  const chartData = points.map((point) => {
    const nextPoint: Record<string, number | string> = {
      ...point,
      chart_time_ms:
        scopeMode === "all" ? new Date(point.timestamp).getTime() - firstTimestamp : point.lap_time_ms,
    };
    for (const signal of selectedSignals) {
      const values = points.map((entry) => Number(entry[signal as keyof TelemetryPoint]));
      const min = Math.min(...values);
      const max = Math.max(...values);
      const value = Number(point[signal as keyof TelemetryPoint]);
      nextPoint[signal] =
        scaleMode === "relative" && max > min ? ((value - min) / (max - min)) * 100 : value;
    }
    return nextPoint;
  });

  return (
    <section className="panel">
      <div className="panel-header split">
        <div>
          <p className="eyebrow">Time-series signals</p>
          <h3>Telemetry Trace</h3>
        </div>
        <div className="chart-controls">
          <div className="signal-toggle-group">
            <button
              type="button"
              className={`signal-chip ${scopeMode === "lap" ? "active" : ""}`}
              onClick={() => onScopeModeChange("lap")}
            >
              Selected Lap
            </button>
            <button
              type="button"
              className={`signal-chip ${scopeMode === "all" ? "active" : ""}`}
              onClick={() => onScopeModeChange("all")}
            >
              All Laps
            </button>
          </div>
          <div className="signal-toggle-group">
            <button
              type="button"
              className={`signal-chip ${scaleMode === "relative" ? "active" : ""}`}
              onClick={() => onScaleModeChange("relative")}
            >
              Relative Scale
            </button>
            <button
              type="button"
              className={`signal-chip ${scaleMode === "raw" ? "active" : ""}`}
              onClick={() => onScaleModeChange("raw")}
            >
              Raw Scale
            </button>
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
      </div>
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="2 6" stroke="#d9d4cc" />
            <XAxis
              dataKey="chart_time_ms"
              stroke="#555"
              tickFormatter={(value) => `${Math.round(Number(value) / 1000)}s`}
            />
            <YAxis
              stroke="#555"
              domain={scaleMode === "relative" ? [0, 100] : ["auto", "auto"]}
              tickFormatter={(value) => (scaleMode === "relative" ? `${value}%` : `${value}`)}
            />
            <Tooltip content={<ChartTooltip />} />
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
