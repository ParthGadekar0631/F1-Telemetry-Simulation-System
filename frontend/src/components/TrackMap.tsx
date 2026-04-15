import type { TelemetryPoint } from "../types/api";


type TrackMapProps = {
  points: TelemetryPoint[];
  activePoint: TelemetryPoint | null;
};

function normalize(points: TelemetryPoint[]) {
  if (points.length === 0) {
    return [];
  }

  const xs = points.map((point) => point.track_x);
  const ys = points.map((point) => point.track_y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);

  return points.map((point) => ({
    x: ((point.track_x - minX) / Math.max(maxX - minX, 1)) * 520 + 40,
    y: ((point.track_y - minY) / Math.max(maxY - minY, 1)) * 260 + 40,
  }));
}


export function TrackMap({ points, activePoint }: TrackMapProps) {
  const normalized = normalize(points);
  const active = activePoint ? normalize([...(points.length ? points : [activePoint]), activePoint]).at(-1) : null;

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Circuit view</p>
          <h3>Track Map</h3>
        </div>
      </div>
      <svg className="track-map" viewBox="0 0 600 340" role="img" aria-label="Track map">
        <defs>
          <linearGradient id="trackGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#18212f" />
            <stop offset="100%" stopColor="#d62939" />
          </linearGradient>
        </defs>
        <rect x="0" y="0" width="600" height="340" rx="24" fill="#f8f1e6" />
        <path
          d={normalized.map((point, index) => `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`).join(" ")}
          fill="none"
          stroke="url(#trackGradient)"
          strokeWidth="10"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        {active ? <circle cx={active.x} cy={active.y} r="11" fill="#ff9f1c" stroke="#ffffff" strokeWidth="4" /> : null}
      </svg>
    </section>
  );
}
