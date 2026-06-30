import React, { createContext, useContext } from "react";

/* ================= TYPES ================= */

export interface AuditLog {
  id: number;
  time: string;
  user: string;
  role: string;
  action: string;
  module: string;
  ip: string;
}

/* ================= MOCK DATA ================= */

const auditLogs: AuditLog[] = [
  {
    id: 1,
    time: "10:42 AM",
    user: "Dr. Sarah Chen",
    role: "Admin",
    action: "Acknowledged critical alert ALT-001",
    module: "Alerts",
    ip: "192.168.0.15",
  },
  {
    id: 2,
    time: "10:38 AM",
    user: "Tom Baker",
    role: "Technician",
    action: "Ran diagnostics on Ventilator DEV-007",
    module: "Device Management",
    ip: "192.168.0.22",
  },
  {
    id: 3,
    time: "10:20 AM",
    user: "Dr. Sarah Chen",
    role: "Admin",
    action: "Registered new ventilator DEV-011",
    module: "Device Management",
    ip: "192.168.0.15",
  },
  {
    id: 4,
    time: "10:05 AM",
    user: "Kevin Lee",
    role: "Hospital IT",
    action: "Updated network gateway GW-02",
    module: "ICU Management",
    ip: "192.168.0.30",
  },
  {
    id: 5,
    time: "9:50 AM",
    user: "Dr. Sarah Chen",
    role: "Admin",
    action: "Created user account for Dr. Patel",
    module: "User Management",
    ip: "192.168.0.15",
  },
  {
    id: 6,
    time: "9:30 AM",
    user: "Maria Rodriguez",
    role: "Nurse",
    action: "Viewed patient vitals ICU-G-01",
    module: "Dashboard",
    ip: "192.168.0.45",
  },
  {
    id: 7,
    time: "9:15 AM",
    user: "Dr. James Wilson",
    role: "Doctor",
    action: "Exported ICU utilization report",
    module: "Reports",
    ip: "192.168.0.18",
  },
];

/* ================= CONTEXT ================= */

const AuditLogContext = createContext<AuditLog[]>(auditLogs);

export const AuditLogProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  return (
    <AuditLogContext.Provider value={auditLogs}>
      {children}
    </AuditLogContext.Provider>
  );
};

export const useAuditLogs = () => useContext(AuditLogContext);