import { useEffect, useMemo, useState, startTransition } from "react";

import { AlertsPanel } from "../components/AlertsPanel";
import { HeroVisual } from "../components/HeroVisual";
import { LapComparisonCard } from "../components/LapComparisonCard";
import { MetricCard } from "../components/MetricCard";
import { ReplayControls } from "../components/ReplayControls";
import { SessionList } from "../components/SessionList";
import { SignalChart, type ChartScaleMode, type ChartScopeMode } from "../components/SignalChart";
import { TrackMap } from "../components/TrackMap";
import { usePolling } from "../hooks/usePolling";
import { api } from "../services/api";
import type {
  Alert,
  Anomaly,
  LapComparison,
  ReplayMetadata,
  SessionAnalytics,
  SessionSummary,
  SectorComparison,
  TelemetryPoint,
} from "../types/api";
import { formatLapTime, formatNumber } from "../utils/formatters";


const DEFAULT_SIGNALS = ["speed_kph", "rpm", "engine_temp_c", "fuel_load_kg"];


export function DashboardPage() {
  const [theme, setTheme] = useState<"light" | "dark">(() => {
    if (typeof window === "undefined") {
      return "light";
    }
    return window.localStorage.getItem("f1-dashboard-theme") === "dark" ? "dark" : "light";
  });
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [selectedCircuit, setSelectedCircuit] = useState("all");
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);
  const [analytics, setAnalytics] = useState<SessionAnalytics | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [currentLapPoints, setCurrentLapPoints] = useState<TelemetryPoint[]>([]);
  const [sessionPoints, setSessionPoints] = useState<TelemetryPoint[]>([]);
  const [replayMetadata, setReplayMetadata] = useState<ReplayMetadata | null>(null);
  const [replayPoints, setReplayPoints] = useState<TelemetryPoint[]>([]);
  const [replayLap, setReplayLap] = useState(1);
  const [replaySpeed, setReplaySpeed] = useState(1);
  const [replayIndex, setReplayIndex] = useState(0);
  const [replayPlaying, setReplayPlaying] = useState(false);
  const [selectedSignals, setSelectedSignals] = useState<string[]>(DEFAULT_SIGNALS);
  const [chartScaleMode, setChartScaleMode] = useState<ChartScaleMode>("relative");
  const [chartScopeMode, setChartScopeMode] = useState<ChartScopeMode>("lap");
  const [lapA, setLapA] = useState(1);
  const [lapB, setLapB] = useState(2);
  const [comparison, setComparison] = useState<LapComparison | null>(null);
  const [sectorComparison, setSectorComparison] = useState<SectorComparison[]>([]);
  const [livePoint, setLivePoint] = useState<TelemetryPoint | null>(null);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    window.localStorage.setItem("f1-dashboard-theme", theme);
  }, [theme]);

  usePolling(async () => {
    const nextSessions = await api.getSessions();
    startTransition(() => {
      setSessions(nextSessions);
      if (!selectedSessionId && nextSessions.length > 0) {
        setSelectedSessionId(nextSessions[0].session_id);
      }
    });
  }, 5000);

  usePolling(
    async () => {
      if (!selectedSessionId) {
        return;
      }

      const [live, nextAnalytics, nextAlerts, nextAnomalies, nextReplayMetadata] = await Promise.all([
        api.getLiveTelemetry(selectedSessionId),
        api.getSessionAnalytics(selectedSessionId),
        api.getAlerts(selectedSessionId),
        api.getAnomalies(selectedSessionId),
        api.getReplayMetadata(selectedSessionId).catch(() => null),
      ]);

      startTransition(() => {
        setLivePoint(live.latest);
        setAnalytics(nextAnalytics);
        setAlerts(nextAlerts);
        setAnomalies(nextAnomalies);
        setReplayMetadata(nextReplayMetadata);
      });

      const targetLapNumber =
        live.is_live && live.latest
          ? live.latest.lap_number
          : nextAnalytics.best_lap_number ?? nextAnalytics.lap_summaries.at(-1)?.lap_number ?? live.latest?.lap_number;

      if (targetLapNumber) {
        const [history, allHistory] = await Promise.all([
          api.getLapHistory(selectedSessionId, targetLapNumber),
          api.getLapHistory(selectedSessionId),
        ]);
        startTransition(() => {
          setCurrentLapPoints(history);
          setSessionPoints(allHistory);
          setLivePoint(history.at(-1) ?? live.latest);
        });
      }
    },
    1500,
    Boolean(selectedSessionId),
  );

  useEffect(() => {
    if (!selectedSessionId || !replayMetadata) {
      return;
    }

    if (!replayMetadata.available_laps.includes(replayLap)) {
      setReplayLap(replayMetadata.available_laps[0] ?? 1);
    }
  }, [selectedSessionId, replayLap, replayMetadata]);

  useEffect(() => {
    if (!selectedSessionId || !replayLap) {
      return;
    }

    void api.getReplayLap(selectedSessionId, replayLap).then((response) => {
      startTransition(() => {
        setReplayPoints(response.points);
        setReplayIndex(0);
      });
    });
  }, [selectedSessionId, replayLap]);

  useEffect(() => {
    if (!selectedSessionId || !analytics || analytics.lap_summaries.length < 2) {
      setComparison(null);
      setSectorComparison([]);
      return;
    }

    void Promise.all([
      api.compareLaps(selectedSessionId, lapA, lapB),
      api.compareSectors(selectedSessionId, lapA, lapB),
    ]).then(([lapResponse, sectorResponse]) => {
      startTransition(() => {
        setComparison(lapResponse);
        setSectorComparison(sectorResponse);
      });
    });
  }, [analytics, lapA, lapB, selectedSessionId]);

  useEffect(() => {
    if (!replayPlaying || replayPoints.length === 0) {
      return;
    }

    const timer = window.setInterval(() => {
      setReplayIndex((current) => {
        if (current >= replayPoints.length - 1) {
          setReplayPlaying(false);
          return current;
        }
        return current + 1;
      });
    }, Math.max(40, 180 / replaySpeed));

    return () => window.clearInterval(timer);
  }, [replayPlaying, replayPoints, replaySpeed]);

  const focusLapNumber = analytics?.best_lap_number ?? livePoint?.lap_number ?? 1;
  const replayViewActive = replayPlaying || replayIndex > 0 || replayLap !== focusLapNumber;
  const replayTracePoints = replayPoints.slice(0, replayIndex + 1);
  const replayCursorPoint = replayTracePoints.at(-1) ?? replayPoints[0] ?? null;
  const replaySessionCutoffIndex =
    replayCursorPoint != null ? sessionPoints.findIndex((point) => point.id === replayCursorPoint.id) : -1;
  const sessionTracePoints =
    replayViewActive && replaySessionCutoffIndex >= 0
      ? sessionPoints.slice(0, replaySessionCutoffIndex + 1)
      : sessionPoints;
  const displayedPoint = replayViewActive ? replayPoints[replayIndex] ?? livePoint : livePoint;
  const chartPoints =
    chartScopeMode === "all"
      ? replayViewActive
        ? sessionTracePoints
        : sessionPoints
      : replayViewActive
        ? replayTracePoints
        : currentLapPoints;
  const trackPoints = replayViewActive ? replayTracePoints : currentLapPoints;
  const lapOptions = analytics?.lap_summaries.map((lap) => lap.lap_number) ?? [1];
  const circuitOptions = useMemo(
    () => [...new Set(sessions.map((session) => session.track_name))].sort((left, right) => left.localeCompare(right)),
    [sessions],
  );
  const filteredSessions = useMemo(
    () => sessions.filter((session) => selectedCircuit === "all" || session.track_name === selectedCircuit),
    [selectedCircuit, sessions],
  );
  const selectedSession = sessions.find((session) => session.session_id === selectedSessionId) ?? null;

  useEffect(() => {
    if (filteredSessions.length === 0) {
      return;
    }

    if (!selectedSessionId || !filteredSessions.some((session) => session.session_id === selectedSessionId)) {
      setSelectedSessionId(filteredSessions[0].session_id);
    }
  }, [filteredSessions, selectedSessionId]);

  useEffect(() => {
    if (lapOptions.length >= 2) {
      setLapA(lapOptions[0]);
      setLapB(lapOptions[1]);
    }
  }, [analytics]);

  const summaryCards = useMemo(
    () => [
      {
        label: "Speed",
        value: `${formatNumber(displayedPoint?.speed_kph, 0)} kph`,
        accent: "#d62939",
      },
      {
        label: "RPM",
        value: `${formatNumber(displayedPoint?.rpm, 0)}`,
        accent: "#18212f",
      },
      {
        label: "Gear",
        value: `${displayedPoint?.gear ?? "--"}`,
        accent: "#ff9f1c",
      },
      {
        label: "Fuel",
        value: `${formatNumber(displayedPoint?.fuel_load_kg, 1)} kg`,
        accent: "#7d5a50",
      },
      {
        label: "Battery",
        value: `${formatNumber(displayedPoint?.battery_pct, 1)} %`,
        accent: "#1d6f42",
      },
      {
        label: "Best Lap",
        value: formatLapTime(analytics?.best_lap_ms),
        accent: "#9f2b68",
      },
    ],
    [analytics?.best_lap_ms, displayedPoint],
  );

  function toggleSignal(signal: string) {
    setSelectedSignals((current) =>
      current.includes(signal) ? current.filter((item) => item !== signal) : [...current, signal],
    );
  }

  return (
    <main className="dashboard-shell">
      <section className="hero">
        <div className="hero-copy-block">
          <p className="eyebrow">F1 Telemetry Simulation System</p>
          <h1>Race engineering dashboard for live telemetry and replay analysis.</h1>
          <p className="hero-copy">
            Stream simulated vehicle state, review prior laps, compare sector delta, and surface alert conditions from a
            single-car telemetry pipeline designed to scale to multi-car operation.
          </p>
          {selectedSession ? (
            <div className="hero-meta">
              <span className="hero-badge">{selectedSession.track_name}</span>
              <span className="hero-badge">{selectedSession.total_laps} laps</span>
              <span className="hero-badge">{selectedSession.weather_condition ?? "Dry"}</span>
              <span className="hero-badge">
                Rain {selectedSession.rain_intensity_pct != null ? `${selectedSession.rain_intensity_pct}%` : "0%"}
              </span>
              <span className="hero-badge">
                Wind {selectedSession.wind_kph != null ? `${selectedSession.wind_kph} kph` : "0 kph"}
              </span>
            </div>
          ) : null}
        </div>
        <div className="hero-side">
          <div className="hero-actions">
            <button
              type="button"
              className="ghost-button"
              onClick={() => setTheme((current) => (current === "light" ? "dark" : "light"))}
            >
              {theme === "light" ? "Dark Mode" : "Light Mode"}
            </button>
            {selectedSessionId ? (
              <>
                <a className="ghost-button" href={api.exportUrl(selectedSessionId, "csv")}>
                  Export CSV
                </a>
                <a className="primary-button" href={api.exportUrl(selectedSessionId, "json")}>
                  Export JSON
                </a>
              </>
            ) : null}
          </div>
          <HeroVisual theme={theme} />
        </div>
      </section>

      <section className="metrics-grid">
        {summaryCards.map((card) => (
          <MetricCard key={card.label} label={card.label} value={card.value} accent={card.accent} />
        ))}
      </section>

      <section className="dashboard-grid">
        <div className="primary-column">
          <SignalChart
            points={chartPoints}
            selectedSignals={selectedSignals}
            onToggleSignal={toggleSignal}
            scaleMode={chartScaleMode}
            onScaleModeChange={setChartScaleMode}
            scopeMode={chartScopeMode}
            onScopeModeChange={setChartScopeMode}
          />
          <LapComparisonCard
            comparison={comparison}
            sectors={sectorComparison}
            lapA={lapA}
            lapB={lapB}
            onLapAChange={setLapA}
            onLapBChange={setLapB}
            lapOptions={lapOptions}
          />
        </div>
        <div className="secondary-column">
          <TrackMap points={trackPoints} activePoint={displayedPoint} trackName={selectedSession?.track_name} />
          <ReplayControls
            lapOptions={replayMetadata?.available_laps ?? [1]}
            selectedLap={replayLap}
            replaySpeed={replaySpeed}
            isPlaying={replayPlaying}
            currentIndex={replayIndex}
            totalPoints={replayPoints.length}
            onLapChange={setReplayLap}
            onReplaySpeedChange={setReplaySpeed}
            onPlayPause={() => setReplayPlaying((current) => !current)}
            onScrub={setReplayIndex}
          />
          <AlertsPanel alerts={alerts} anomalies={anomalies} />
        </div>
      </section>

      <section className="session-row">
        <SessionList
          sessions={filteredSessions}
          selectedSessionId={selectedSessionId}
          selectedCircuit={selectedCircuit}
          circuitOptions={circuitOptions}
          onSelectCircuit={setSelectedCircuit}
          onSelect={setSelectedSessionId}
        />
        <section className="panel summary-panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Session analytics</p>
              <h3>Performance Overview</h3>
            </div>
          </div>
          <div className="summary-grid">
            <article>
              <span>Peak Speed</span>
              <strong>{formatNumber(analytics?.peak_speed_kph)} kph</strong>
            </article>
            <article>
              <span>Average Lap</span>
              <strong>{formatLapTime(analytics?.average_lap_ms ?? null)}</strong>
            </article>
            <article>
              <span>Fuel Burn</span>
              <strong>{formatNumber(analytics?.total_fuel_burn_kg, 2)} kg</strong>
            </article>
            <article>
              <span>Energy Used</span>
              <strong>{formatNumber(analytics?.total_energy_used_kj)} kJ</strong>
            </article>
            <article>
              <span>Avg Engine Temp</span>
              <strong>{formatNumber(analytics?.average_engine_temp_c)} C</strong>
            </article>
            <article>
              <span>Braking Zones</span>
              <strong>{analytics?.braking_zones_detected ?? "--"}</strong>
            </article>
          </div>
        </section>
      </section>
    </main>
  );
}
