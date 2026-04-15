import { useId } from "react";


type HeroVisualProps = {
  theme: "light" | "dark";
};


export function HeroVisual({ theme }: HeroVisualProps) {
  const checkerId = useId().replace(/:/g, "");
  const glowId = useId().replace(/:/g, "");

  return (
    <div className="hero-visual" aria-hidden="true">
      <svg viewBox="0 0 520 340" className="hero-visual-svg">
        <defs>
          <pattern id={checkerId} width="24" height="24" patternUnits="userSpaceOnUse">
            <rect width="24" height="24" fill={theme === "dark" ? "#161a24" : "#f4eee2"} />
            <rect width="12" height="12" fill={theme === "dark" ? "#d7dde8" : "#121a28"} opacity="0.18" />
            <rect x="12" y="12" width="12" height="12" fill={theme === "dark" ? "#d7dde8" : "#121a28"} opacity="0.18" />
          </pattern>
          <linearGradient id={glowId} x1="10%" y1="10%" x2="100%" y2="90%">
            <stop offset="0%" stopColor="var(--hero-accent)" />
            <stop offset="100%" stopColor="var(--hero-accent-alt)" />
          </linearGradient>
        </defs>

        <rect x="0" y="0" width="520" height="340" rx="28" fill="var(--hero-panel)" />
        <rect x="28" y="28" width="132" height="72" rx="18" fill={`url(#${checkerId})`} opacity="0.95" />
        <rect x="360" y="40" width="132" height="72" rx="18" fill={`url(#${checkerId})`} opacity="0.95" />

        <g transform="translate(38 118)">
          <path
            d="M 32 88 C 56 53 94 34 150 27 L 224 18 C 273 12 309 21 342 44 L 408 90 C 433 107 446 130 442 153 C 437 178 415 197 381 204 L 338 212 C 320 215 307 223 300 237 L 288 258 L 230 258 L 217 226 L 132 226 L 110 258 L 52 258 L 78 205 L 40 191 C 14 182 1 164 3 140 C 6 117 16 102 32 88 Z"
            fill={`url(#${glowId})`}
          />
          <circle cx="120" cy="240" r="32" fill="#0f1420" />
          <circle cx="335" cy="240" r="32" fill="#0f1420" />
          <circle cx="120" cy="240" r="15" fill="#f7f5ef" opacity="0.9" />
          <circle cx="335" cy="240" r="15" fill="#f7f5ef" opacity="0.9" />
          <path d="M 114 44 L 214 34 L 246 84 L 168 96 L 114 86 Z" fill="rgba(255,255,255,0.24)" />
          <path d="M 282 56 L 350 64 L 390 100 L 322 106 Z" fill="rgba(255,255,255,0.14)" />
          <path d="M 25 165 L 75 148 L 95 184 L 37 195 Z" fill="rgba(255,255,255,0.18)" />
        </g>

        <text x="36" y="311" className="hero-visual-copy">
          CURRENT 2026 F1 CIRCUITS · LIVE TELEMETRY · REPLAY DELTA
        </text>
      </svg>
    </div>
  );
}
