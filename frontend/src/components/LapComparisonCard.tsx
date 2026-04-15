import type { LapComparison, SectorComparison } from "../types/api";
import { formatLapTime, formatNumber, formatSignedMilliseconds } from "../utils/formatters";


type LapComparisonCardProps = {
  comparison: LapComparison | null;
  sectors: SectorComparison[];
  lapA: number;
  lapB: number;
  onLapAChange: (lap: number) => void;
  onLapBChange: (lap: number) => void;
  lapOptions: number[];
};


export function LapComparisonCard({
  comparison,
  sectors,
  lapA,
  lapB,
  onLapAChange,
  onLapBChange,
  lapOptions,
}: LapComparisonCardProps) {
  return (
    <section className="panel">
      <div className="panel-header split">
        <div>
          <p className="eyebrow">Run comparison</p>
          <h3>Lap Delta</h3>
        </div>
        <div className="comparison-pickers">
          <select value={lapA} onChange={(event) => onLapAChange(Number(event.target.value))}>
            {lapOptions.map((lap) => (
              <option key={`a-${lap}`} value={lap}>
                Lap {lap}
              </option>
            ))}
          </select>
          <select value={lapB} onChange={(event) => onLapBChange(Number(event.target.value))}>
            {lapOptions.map((lap) => (
              <option key={`b-${lap}`} value={lap}>
                Lap {lap}
              </option>
            ))}
          </select>
        </div>
      </div>
      {comparison ? (
        <div className="comparison-grid">
          <article className="comparison-stat">
            <span>Lap A</span>
            <strong>{formatLapTime(comparison.lap_a_time_ms)}</strong>
          </article>
          <article className="comparison-stat">
            <span>Lap B</span>
            <strong>{formatLapTime(comparison.lap_b_time_ms)}</strong>
          </article>
          <article className="comparison-stat">
            <span>Delta</span>
            <strong>{formatSignedMilliseconds(comparison.lap_delta_ms)}</strong>
          </article>
          <article className="comparison-stat">
            <span>Top Speed Delta</span>
            <strong>{formatNumber(comparison.top_speed_delta_kph)} kph</strong>
          </article>
          <article className="comparison-stat">
            <span>Fuel Delta</span>
            <strong>{formatNumber(comparison.fuel_delta_kg, 2)} kg</strong>
          </article>
          <article className="comparison-stat">
            <span>Energy Delta</span>
            <strong>{formatNumber(comparison.energy_delta_kj)} kJ</strong>
          </article>
          {sectors.map((sector) => (
            <article key={sector.sector_number} className="sector-row">
              <span>Sector {sector.sector_number}</span>
              <strong>{formatSignedMilliseconds(sector.delta_ms)}</strong>
            </article>
          ))}
        </div>
      ) : (
        <p className="empty-state">Load at least two completed laps to compare deltas.</p>
      )}
    </section>
  );
}
