import { useEffect, useEffectEvent } from "react";


export function usePolling(callback: () => void | Promise<void>, intervalMs: number, enabled = true) {
  const onTick = useEffectEvent(callback);

  useEffect(() => {
    if (!enabled) {
      return;
    }

    void onTick();
    const timer = window.setInterval(() => {
      void onTick();
    }, intervalMs);

    return () => window.clearInterval(timer);
  }, [enabled, intervalMs, onTick]);
}
