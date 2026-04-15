export function formatLapTime(milliseconds: number | null | undefined): string {
  if (milliseconds == null) {
    return "--";
  }

  const totalSeconds = milliseconds / 1000;
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = (totalSeconds % 60).toFixed(3).padStart(6, "0");
  return `${minutes}:${seconds}`;
}

export function formatSignedMilliseconds(milliseconds: number): string {
  const prefix = milliseconds > 0 ? "+" : "";
  return `${prefix}${(milliseconds / 1000).toFixed(3)}s`;
}

export function formatNumber(value: number | null | undefined, digits = 1): string {
  if (value == null || Number.isNaN(value)) {
    return "--";
  }
  return value.toFixed(digits);
}
