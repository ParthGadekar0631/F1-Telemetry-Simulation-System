import { useId } from "react";


type HeroVisualProps = {
  theme: "light" | "dark";
};


export function HeroVisual({ theme }: HeroVisualProps) {
  const checkerId = useId().replace(/:/g, "");
  const glowId = useId().replace(/:/g, "");
  const flagId = useId().replace(/:/g, "");

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
          <linearGradient id={flagId} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="0.95" />
            <stop offset="100%" stopColor="#d9dde6" stopOpacity="0.8" />
          </linearGradient>
        </defs>

        <rect x="0" y="0" width="520" height="340" rx="28" fill="var(--hero-panel)" />
        <rect x="28" y="28" width="132" height="72" rx="18" fill={`url(#${checkerId})`} opacity="0.95" />
        <rect x="360" y="40" width="132" height="72" rx="18" fill={`url(#${checkerId})`} opacity="0.95" />

        <g transform="translate(42 30)">
          <rect x="0" y="6" width="4" height="58" rx="2" fill="var(--muted)" opacity="0.85" />
          <path d="M 6 10 C 44 4 68 19 95 12 L 95 52 C 67 60 44 44 6 50 Z" fill={`url(#${flagId})`} />
          <path d="M 12 16 H 28 V 32 H 12 Z M 28 32 H 44 V 48 H 28 Z M 44 16 H 60 V 32 H 44 Z M 60 32 H 76 V 48 H 60 Z" fill="#121a28" opacity="0.8" />
        </g>

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
          <path d="M 26 126 C 86 96 132 90 176 94" fill="none" stroke="rgba(255,255,255,0.25)" strokeWidth="6" strokeLinecap="round" />
          <path d="M 300 128 C 350 110 385 113 424 128" fill="none" stroke="rgba(255,255,255,0.22)" strokeWidth="5" strokeLinecap="round" />
        </g>

        <g transform="translate(338 246)">
          <rect x="0" y="0" width="126" height="50" rx="18" fill="rgba(255,255,255,0.08)" />
          <path d="M 20 32 H 102" stroke="var(--track-trail)" strokeWidth="4" strokeLinecap="round" />
          <path d="M 27 14 L 44 14 L 49 24 L 77 24 L 86 16 L 96 16 L 101 22 L 95 30 L 84 30 L 78 36 L 58 36 L 53 30 L 34 30 L 27 26 Z" fill="var(--hero-accent-alt)" />
          <circle cx="42" cy="36" r="6" fill="#11161f" />
          <circle cx="77" cy="36" r="6" fill="#11161f" />
        </g>

        <text x="36" y="311" className="hero-visual-copy">
          CURRENT 2026 F1 CIRCUITS | LIVE TELEMETRY | REPLAY DELTA
        </text>
      </svg>
    </div>
  );
}
