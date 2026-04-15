import type {
  Alert,
  Anomaly,
  LapComparison,
  LiveTelemetryResponse,
  ReplayMetadata,
  ReplayResponse,
  SectorComparison,
  SessionAnalytics,
  SessionSummary,
  TelemetryPoint,
} from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`API request failed for ${path}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  getSessions: () => getJson<SessionSummary[]>("/sessions"),
  getLiveTelemetry: (sessionId: string) => getJson<LiveTelemetryResponse>(`/telemetry/live?session_id=${sessionId}`),
  getLatestTelemetry: (sessionId: string) => getJson<TelemetryPoint>(`/telemetry/latest/${sessionId}`),
  getLapHistory: (sessionId: string, lapNumber: number) =>
    getJson<TelemetryPoint[]>(`/telemetry/history/${sessionId}?lap_number=${lapNumber}`),
  getSessionAnalytics: (sessionId: string) =>
    getJson<SessionAnalytics>(`/analytics/sessions/${sessionId}/summary`),
  compareLaps: (sessionId: string, lapA: number, lapB: number) =>
    getJson<LapComparison>(`/analytics/sessions/${sessionId}/laps/compare?lap_a=${lapA}&lap_b=${lapB}`),
  compareSectors: (sessionId: string, lapA: number, lapB: number) =>
    getJson<SectorComparison[]>(`/analytics/sessions/${sessionId}/sectors/compare?lap_a=${lapA}&lap_b=${lapB}`),
  getAlerts: (sessionId: string) => getJson<Alert[]>(`/alerts?session_id=${sessionId}`),
  getAnomalies: (sessionId: string) => getJson<Anomaly[]>(`/anomalies?session_id=${sessionId}`),
  getReplayMetadata: (sessionId: string) => getJson<ReplayMetadata>(`/replay/${sessionId}`),
  getReplayLap: (sessionId: string, lapNumber: number) =>
    getJson<ReplayResponse>(`/replay/${sessionId}/laps/${lapNumber}`),
  exportUrl: (sessionId: string, format: "csv" | "json") =>
    `${API_BASE_URL}/exports/${sessionId}?format=${format}`,
};
