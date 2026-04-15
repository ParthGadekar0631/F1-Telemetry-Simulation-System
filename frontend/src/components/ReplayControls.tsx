type ReplayControlsProps = {
  lapOptions: number[];
  selectedLap: number;
  replaySpeed: number;
  isPlaying: boolean;
  currentIndex: number;
  totalPoints: number;
  onLapChange: (lap: number) => void;
  onReplaySpeedChange: (speed: number) => void;
  onPlayPause: () => void;
  onScrub: (index: number) => void;
};


export function ReplayControls({
  lapOptions,
  selectedLap,
  replaySpeed,
  isPlaying,
  currentIndex,
  totalPoints,
  onLapChange,
  onReplaySpeedChange,
  onPlayPause,
  onScrub,
}: ReplayControlsProps) {
  return (
    <section className="panel">
      <div className="panel-header split">
        <div>
          <p className="eyebrow">Replay mode</p>
          <h3>Lap Playback</h3>
        </div>
      </div>
      <div className="replay-controls">
        <label>
          Lap
          <select value={selectedLap} onChange={(event) => onLapChange(Number(event.target.value))}>
            {lapOptions.map((lap) => (
              <option key={lap} value={lap}>
                Lap {lap}
              </option>
            ))}
          </select>
        </label>
        <label>
          Speed
          <select value={replaySpeed} onChange={(event) => onReplaySpeedChange(Number(event.target.value))}>
            {[0.5, 1, 1.5, 2, 4].map((speed) => (
              <option key={speed} value={speed}>
                {speed}x
              </option>
            ))}
          </select>
        </label>
        <button type="button" className="primary-button" onClick={onPlayPause}>
          {isPlaying ? "Pause" : "Play"}
        </button>
      </div>
      <input
        className="timeline-slider"
        type="range"
        min={0}
        max={Math.max(totalPoints - 1, 0)}
        value={currentIndex}
        onChange={(event) => onScrub(Number(event.target.value))}
      />
    </section>
  );
}
