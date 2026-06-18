import { useEffect, useRef } from "react";

/** Snapshot broadcast by the backend (snake_case, matches LatestVital). */
export interface LiveVitalSnapshot {
  hr: number | null;
  bp_sys: number | null;
  bp_dia: number | null;
  spo2: number | null;
  temp: number | null;
  rr: number | null;
  status: string | null;
}

export interface LiveVitalMessage {
  type: "LIVE_VITAL_UPDATE";
  patient_id: number;
  bed_id: number;
  unit_id: number;
  metric: string;
  value: number;
  recorded_at: string;
  snapshot: LiveVitalSnapshot;
}

export interface LiveAlarmMessage {
  type: "LIVE_ALARM_UPDATE";
  unit_id: number;
  patient_id: number;
  patient_name: string;
  bed_id: string;
  severity: string;
  message: string;
}

function buildWsUrl(unitId: number): string {
  const base =
    import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";
  const wsBase = base.replace(/^http/i, "ws");
  return `${wsBase}/ws/live-vitals/${unitId}`;
}

/**
 * Subscribe to the unit-scoped live-vitals WebSocket stream.
 *
 * Reconnects automatically on drop and sends a keep-alive ping every 30s.
 * Callbacks are held in refs so updating them does not reconnect the socket.
 */
export function useLiveVitals(
  unitId: number | null | undefined,
  onVital: (msg: LiveVitalMessage) => void,
  onAlarm?: (msg: LiveAlarmMessage) => void
): void {
  const vitalRef = useRef(onVital);
  const alarmRef = useRef(onAlarm);
  vitalRef.current = onVital;
  alarmRef.current = onAlarm;

  useEffect(() => {
    if (unitId == null) return;

    let ws: WebSocket | null = null;
    let pingTimer: ReturnType<typeof setInterval> | null = null;
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
    let closed = false;

    function connect() {
      if (closed) return;
      ws = new WebSocket(buildWsUrl(unitId as number));

      ws.onopen = () => {
        pingTimer = setInterval(() => {
          if (ws && ws.readyState === WebSocket.OPEN) ws.send("ping");
        }, 30_000);
      };

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          if (msg.type === "LIVE_VITAL_UPDATE") {
            vitalRef.current(msg as LiveVitalMessage);
          } else if (msg.type === "LIVE_ALARM_UPDATE") {
            alarmRef.current?.(msg as LiveAlarmMessage);
          }
        } catch {
          // ignore malformed frames
        }
      };

      ws.onclose = () => {
        if (pingTimer) clearInterval(pingTimer);
        if (!closed) {
          reconnectTimer = setTimeout(connect, 3_000);
        }
      };

      ws.onerror = () => {
        ws?.close();
      };
    }

    connect();

    return () => {
      closed = true;
      if (pingTimer) clearInterval(pingTimer);
      if (reconnectTimer) clearTimeout(reconnectTimer);
      ws?.close();
    };
  }, [unitId]);
}
