import { useEffect, useRef, useState } from "react";

import type { TelemetryPoint } from "../types/api";
import { getCircuitDefinition } from "../utils/circuits";


type TrackMapProps = {
  points: TelemetryPoint[];
  activePoint: TelemetryPoint | null;
  trackName?: string | null;
};

type SvgPoint = {
  x: number;
  y: number;
};


function buildPolyline(path: SVGPathElement, totalLength: number, progress: number) {
  const steps = Math.max(24, Math.round(progress * 80));
  const points: string[] = [];
  for (let index = 0; index <= steps; index += 1) {
    const point = path.getPointAtLength((totalLength * progress * index) / steps);
    points.push(`${point.x},${point.y}`);
  }
  return points.join(" ");
}


export function TrackMap({ points, activePoint, trackName }: TrackMapProps) {
  const circuit = getCircuitDefinition(trackName);
  const pathRef = useRef<SVGPathElement | null>(null);
  const [carPosition, setCarPosition] = useState<SvgPoint | null>(null);
  const [trailPolyline, setTrailPolyline] = useState("");
  const [sectorMarkers, setSectorMarkers] = useState<SvgPoint[]>([]);

  useEffect(() => {
    if (!pathRef.current) {
      return;
    }

    const path = pathRef.current;
    const totalLength = path.getTotalLength();
    const markers = [0.0, 0.333, 0.666].map((progress) => path.getPointAtLength(totalLength * progress));
    setSectorMarkers(markers);
  }, [circuit.id]);

  useEffect(() => {
    if (!pathRef.current || !activePoint) {
      return;
    }

    const path = pathRef.current;
    const totalLength = path.getTotalLength();
    const progress = Math.min(Math.max(activePoint.lap_distance_pct, 0), 0.999);
    const point = path.getPointAtLength(totalLength * progress);
    setCarPosition({ x: point.x, y: point.y });
    setTrailPolyline(buildPolyline(path, totalLength, progress));
  }, [activePoint, circuit.id]);

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Circuit view</p>
          <h3>Track Map</h3>
          <small className="track-subtitle">{circuit.displayName}</small>
        </div>
      </div>
      <svg className="track-map" viewBox="0 0 960 620" role="img" aria-label={`${circuit.displayName} track map`}>
        <defs>
          <linearGradient id="trackGlow" x1="10%" y1="10%" x2="90%" y2="90%">
            <stop offset="0%" stopColor="var(--track-grad-start)" />
            <stop offset="100%" stopColor="var(--track-grad-end)" />
          </linearGradient>
          <filter id="trackShadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="12" stdDeviation="10" floodColor="rgba(0,0,0,0.22)" />
          </filter>
        </defs>
        <rect x="0" y="0" width="960" height="620" rx="28" fill="var(--track-surface)" />
        <g opacity="0.55">
          {Array.from({ length: 16 }).map((_, index) => (
            <line
              key={`grid-y-${index}`}
              x1="40"
              y1={60 + index * 32}
              x2="920"
              y2={60 + index * 32}
              stroke="var(--track-grid)"
              strokeDasharray="4 10"
            />
          ))}
          {Array.from({ length: 22 }).map((_, index) => (
            <line
              key={`grid-x-${index}`}
              x1={60 + index * 40}
              y1="40"
              x2={60 + index * 40}
              y2="580"
              stroke="var(--track-grid)"
              strokeDasharray="4 10"
            />
          ))}
        </g>
        <path
          ref={pathRef}
          d={circuit.path}
          fill="none"
          stroke="var(--track-outline)"
          strokeWidth="34"
          strokeLinecap="round"
          strokeLinejoin="round"
          opacity="0.85"
        />
        <path
          d={circuit.path}
          fill="none"
          stroke="url(#trackGlow)"
          strokeWidth="16"
          strokeLinecap="round"
          strokeLinejoin="round"
          filter="url(#trackShadow)"
        />
        {trailPolyline ? (
          <polyline
            points={trailPolyline}
            fill="none"
            stroke="var(--track-trail)"
            strokeWidth="10"
            strokeLinecap="round"
            strokeLinejoin="round"
            opacity="0.95"
          />
        ) : null}
        {sectorMarkers.map((marker, index) => (
          <g key={`sector-${index}`} transform={`translate(${marker.x} ${marker.y})`}>
            <circle r="13" fill="var(--track-sector-fill)" stroke="var(--track-sector-stroke)" strokeWidth="4" />
            <text y="5" textAnchor="middle" className="track-sector-label">
              {index + 1}
            </text>
          </g>
        ))}
        <g transform="translate(137 171) rotate(90)">
          <rect x="-26" y="-7" width="52" height="14" fill="var(--track-line)" />
          <rect x="-14" y="-7" width="7" height="14" fill="var(--track-surface)" />
          <rect x="0" y="-7" width="7" height="14" fill="var(--track-surface)" />
          <rect x="14" y="-7" width="7" height="14" fill="var(--track-surface)" />
        </g>
        {carPosition ? (
          <g
            className="track-car"
            transform={`translate(${carPosition.x} ${carPosition.y})`}
            style={{ transition: "transform 180ms linear" }}
          >
            <circle r="18" fill="var(--car-glow)" opacity="0.22" />
            <circle r="10" fill="var(--car-fill)" stroke="white" strokeWidth="4" />
            <path d="M -16 0 L 0 -22 L 16 0 L 0 22 Z" fill="none" stroke="var(--car-accent)" strokeWidth="3" />
          </g>
        ) : null}
        {!activePoint && points.length === 0 ? (
          <text x="480" y="560" textAnchor="middle" className="track-empty-label">
            Waiting for telemetry samples
          </text>
        ) : null}
      </svg>
    </section>
  );
}
