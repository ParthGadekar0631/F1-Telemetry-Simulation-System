type MetricCardProps = {
  label: string;
  value: string;
  accent?: string;
  helper?: string;
};


export function MetricCard({ label, value, accent = "var(--accent)", helper }: MetricCardProps) {
  return (
    <article className="metric-card" style={{ ["--metric-accent" as string]: accent }}>
      <p className="metric-label">{label}</p>
      <strong className="metric-value">{value}</strong>
      {helper ? <span className="metric-helper">{helper}</span> : null}
    </article>
  );
}
