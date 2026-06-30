import React, { createContext, useContext } from "react";

/* ================= TYPES ================= */

export interface HospitalSync {
  id: number;
  name: string;
  city: string;
  status: "Connected" | "Delayed";
  lastSync: string;
  data: string;
}

export interface CloudSummary {
  lastSync: string;
  dataSent: string;
  errors: number;
  hospitals: number;
}

/* ================= MOCK DATA ================= */

const summary: CloudSummary = {
  lastSync: "2 min ago",
  dataSent: "2.74 GB",
  errors: 1,
  hospitals: 3,
};

const hospitalData: HospitalSync[] = [
  {
    id: 1,
    name: "Metro General Hospital",
    city: "New York",
    status: "Connected",
    lastSync: "2 min ago",
    data: "1.2 GB",
  },
  {
    id: 2,
    name: "St. Mary's Medical Center",
    city: "Chicago",
    status: "Connected",
    lastSync: "5 min ago",
    data: "890 MB",
  },
  {
    id: 3,
    name: "Pacific Health Institute",
    city: "San Francisco",
    status: "Delayed",
    lastSync: "25 min ago",
    data: "650 MB",
  },
];

/* ================= CONTEXT ================= */

const CloudSyncContext = createContext({
  summary,
  hospitalData,
});

export const CloudSyncProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  return (
    <CloudSyncContext.Provider value={{ summary, hospitalData }}>
      {children}
    </CloudSyncContext.Provider>
  );
};

export const useCloudSync = () => useContext(CloudSyncContext);