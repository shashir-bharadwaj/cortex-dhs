import React, { createContext, useContext } from "react";

/* ================= MOCK DATA ================= */

const stats = {
  hospitals: 3,
  icuUnits: 5,
  beds: 65,
  connected: 238,
  offline: 12,
  patients: 42,
  critical: 3,
};

const connectivityTrend = [
  { time: "00:00", online: 230, offline: 20 },
  { time: "04:00", online: 228, offline: 22 },
  { time: "08:00", online: 235, offline: 15 },
  { time: "12:00", online: 240, offline: 10 },
  { time: "16:00", online: 238, offline: 12 },
  { time: "20:00", online: 236, offline: 14 },
  { time: "Now", online: 239, offline: 13 },
];

const alertsData = [
  { time: "6 AM", critical: 1, warning: 3, info: 5 },
  { time: "8 AM", critical: 2, warning: 4, info: 3 },
  { time: "10 AM", critical: 3, warning: 2, info: 4 },
  { time: "12 PM", critical: 1, warning: 5, info: 2 },
];

const liveAlerts = [
  {
    bed: "ICU-S-01",
    type: "Warning",
    message: "Patient Monitor: Tachycardia Detected",
    time: "10:38 AM",
  },
  {
    bed: "ICU-C-02",
    type: "Critical",
    message: "ECG Monitor: Irregular Heart Rhythm",
    time: "10:30 AM",
  },
];

const DashboardContext = createContext({
  stats,
  connectivityTrend,
  alertsData,
  liveAlerts,
});

export const DashboardProvider = ({ children }: any) => (
  <DashboardContext.Provider
    value={{ stats, connectivityTrend, alertsData, liveAlerts }}
  >
    {children}
  </DashboardContext.Provider>
);

export const useDashboard = () => useContext(DashboardContext);