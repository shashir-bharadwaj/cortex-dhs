import React, { createContext, useContext } from "react";

/* ================= TYPES ================= */

export interface Device {
  id: string;
  type: string;
  bed: string;
  status: "Online" | "Offline" | "Error";
  lastSync: string;
  ip: string;
}

export interface Timeline {
  time: string;
  online: number;
  offline: number;
}

/* ================= MOCK DATA ================= */

const summary = {
  online: 7,
  offline: 3,
  dataRate: "1.2 Gbps",
  latency: "12ms",
};

const timeline: Timeline[] = [
  { time: "00:00", online: 235, offline: 20 },
  { time: "04:00", online: 234, offline: 22 },
  { time: "08:00", online: 238, offline: 15 },
  { time: "12:00", online: 240, offline: 10 },
  { time: "16:00", online: 238, offline: 12 },
  { time: "20:00", online: 237, offline: 14 },
  { time: "Now", online: 239, offline: 13 },
];

const devices: Device[] = [
  { id: "DEV-001", type: "Patient Monitor", bed: "ICU-C-01", status: "Online", lastSync: "30 sec ago", ip: "192.168.1.101" },
  { id: "DEV-002", type: "Ventilator", bed: "ICU-C-01", status: "Online", lastSync: "1 min ago", ip: "192.168.1.102" },
  { id: "DEV-003", type: "ECG Monitor", bed: "ICU-C-02", status: "Online", lastSync: "45 sec ago", ip: "192.168.1.103" },
  { id: "DEV-004", type: "Infusion Pump", bed: "ICU-C-02", status: "Online", lastSync: "2 min ago", ip: "192.168.1.104" },
  { id: "DEV-005", type: "SpO2 Monitor", bed: "ICU-C-03", status: "Offline", lastSync: "25 min ago", ip: "192.168.1.105" },
  { id: "DEV-006", type: "Temperature Monitor", bed: "ICU-G-01", status: "Online", lastSync: "1 min ago", ip: "192.168.1.106" },
  { id: "DEV-007", type: "Ventilator", bed: "ICU-G-03", status: "Error", lastSync: "15 min ago", ip: "192.168.1.107" },
  { id: "DEV-008", type: "Patient Monitor", bed: "ICU-N-01", status: "Online", lastSync: "20 sec ago", ip: "192.168.1.108" },
  { id: "DEV-009", type: "ECG Monitor", bed: "ICU-S-01", status: "Online", lastSync: "40 sec ago", ip: "192.168.1.109" },
];

/* ================= CONTEXT ================= */

const ConnectivityContext = createContext({
  summary,
  timeline,
  devices,
});

export const ConnectivityProvider = ({ children }: any) => {
  return (
    <ConnectivityContext.Provider value={{ summary, timeline, devices }}>
      {children}
    </ConnectivityContext.Provider>
  );
};

export const useConnectivity = () => useContext(ConnectivityContext);