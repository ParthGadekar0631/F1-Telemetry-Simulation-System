import type { Alert, Anomaly } from "../types/api";


type AlertsPanelProps = {
  alerts: Alert[];
  anomalies: Anomaly[];
};


export function AlertsPanel({ alerts, anomalies }: AlertsPanelProps) {
  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Alerts & anomalies</p>
          <h3>Incident Surface</h3>
        </div>
      </div>
      <div className="incident-list">
        {[...alerts, ...anomalies]
          .slice(0, 8)
          .map((item) => (
            <article key={`${"severity" in item ? "alert" : "anomaly"}-${item.id}`} className="incident-card">
              <span className={`incident-tag ${"severity" in item ? item.severity : "anomaly"}`}>
                {"severity" in item ? item.severity : item.anomaly_type}
              </span>
              <strong>{("message" in item ? item.message : item.description) ?? "Unknown incident"}</strong>
              <small>
                Lap {item.lap_number ?? "-"} | {item.metric_name} | {item.metric_value.toFixed(1)}
              </small>
            </article>
          ))}
      </div>
    </section>
  );
}
