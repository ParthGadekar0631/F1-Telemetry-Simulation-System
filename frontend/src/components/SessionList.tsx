import type { SessionSummary } from "../types/api";
import { formatLapTime } from "../utils/formatters";


type SessionListProps = {
  sessions: SessionSummary[];
  selectedSessionId: string | null;
  onSelect: (sessionId: string) => void;
};


export function SessionList({ sessions, selectedSessionId, onSelect }: SessionListProps) {
  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Session history</p>
          <h3>Runs</h3>
        </div>
      </div>
      <div className="session-list">
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
