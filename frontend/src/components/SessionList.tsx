import type { SessionSummary } from "../types/api";
import { formatLapTime } from "../utils/formatters";


type SessionListProps = {
  sessions: SessionSummary[];
  selectedSessionId: string | null;
  selectedCircuitId: string;
  circuitOptions: Array<{ id: string; displayName: string }>;
  onSelectCircuit: (circuitId: string) => void;
  onSelect: (sessionId: string) => void;
};


export function SessionList({
  sessions,
  selectedSessionId,
  selectedCircuitId,
  circuitOptions,
  onSelectCircuit,
  onSelect,
}: SessionListProps) {
  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Session history</p>
          <h3>Runs</h3>
        </div>
      </div>
      <div className="session-filter-row">
        <label>
          Circuit
          <select value={selectedCircuitId} onChange={(event) => onSelectCircuit(event.target.value)}>
            <option value="all">All circuits</option>
            {circuitOptions.map((circuit) => (
              <option key={circuit.id} value={circuit.id}>
                {circuit.displayName}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div className="session-list">
        {sessions.length === 0 ? <p className="empty-state">No stored sessions for the selected circuit yet.</p> : null}
        {sessions.map((session) => (
          <button
            key={session.session_id}
            className={`session-card ${selectedSessionId === session.session_id ? "active" : ""}`}
            type="button"
            onClick={() => onSelect(session.session_id)}
          >
            <div>
              <strong>{session.name}</strong>
              <p>{session.track_name}</p>
              <small>
                {session.weather_condition ?? "Dry"} | {session.total_laps} laps | Wind {session.wind_kph ?? 0} kph
              </small>
            </div>
            <div>
              <span>{session.status}</span>
              <small>Best {formatLapTime(session.best_lap_ms)}</small>
            </div>
          </button>
        ))}
      </div>
    </section>
  );
}
