import React, { createContext, useContext } from "react";

/* ================= MOCK DATA ================= */

const reportCards = [
  { title: "ICU Utilization", desc: "Utilization rates across all ICU units" },
  { title: "Bed Occupancy", desc: "Bed occupancy trends and statistics" },
  { title: "Device Downtime", desc: "Device offline time and maintenance logs" },
  { title: "Alert Frequency", desc: "Alert patterns and severity distribution" },
  { title: "Patient Monitoring", desc: "Patient data flow and monitoring reports" },
];

const icuData = [
  { name: "General ICU", value: 14 },
  { name: "Cardiac ICU", value: 10 },
  { name: "Surgical ICU", value: 7 },
  { name: "Pediatric ICU", value: 6 },
  { name: "Neonatal ICU", value: 12 },
];

const alertData = [
  { time: "6 AM", critical: 1, warning: 3, info: 5 },
  { time: "8 AM", critical: 2, warning: 4, info: 3 },
  { time: "10 AM", critical: 3, warning: 2, info: 4 },
  { time: "12 PM", critical: 1, warning: 5, info: 2 },
  { time: "2 PM", critical: 2, warning: 3, info: 6 },
  { time: "4 PM", critical: 1, warning: 4, info: 3 },
  { time: "6 PM", critical: 2, warning: 2, info: 4 },
  { time: "8 PM", critical: 3, warning: 3, info: 2 },
];

const ReportsContext = createContext({
  reportCards,
  icuData,
  alertData,
});

export const ReportsProvider = ({ children }: any) => {
  return (
    <ReportsContext.Provider value={{ reportCards, icuData, alertData }}>
      {children}
    </ReportsContext.Provider>
  );
};

export const useReports = () => useContext(ReportsContext);