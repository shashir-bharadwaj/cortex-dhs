export interface ICUUnitMaster {
  id: number;
  icu_name: string;
  type: string;
  department: string;
  beds: number;
  devices: string;
  gateway: string;
  status: string;
}

export interface ICUUnit {
  id: number;
  name: string;
  department?: string;
  totalBeds: number;
  occupiedBeds: number;
}

export interface DashboardSummary {
  normal: number;
  warning: number;
  critical: number;
  activeAlarms: number;
}

export interface VitalReading {
  value?: number | string | null;
  unit: string;
  status: "normal" | "warning" | "critical";
  recordedAt?: string;
}

export interface PatientVitals {
  hr?: VitalReading | null;
  spo2?: VitalReading | null;
  bp?: VitalReading | null;
  rr?: VitalReading | null;
  temp?: VitalReading | null;
}

export interface DashboardBed {
  id: number;
  bedId: string;
}

export interface DashboardPatient {
  id: number;
  name: string;
  age?: number | null;
  gender?: string | null;
  diagnosis?: string | null;
  doctor?: string | null;
}

export interface PatientCard {
  bed: DashboardBed;
  patient?: DashboardPatient | null;
  status: "normal" | "warning" | "critical";
  vitals?: PatientVitals | null;
  monitoring: string[];
  activeAlarmCount: number;
  hasCriticalAlarm: boolean;
}

export interface DashboardAlarm {
  id: number;
  patientId: number;
  patientName: string;
  bedId: string;
  alarmType: string;
  deviceSource: string;
  message: string;
  severity: string;
  timestamp: string;
  acknowledged: boolean;
  silenced: boolean;
  escalated: boolean;
}

export interface DashboardOverview {
  unit: ICUUnit;
  summary: DashboardSummary;
  patientCards: PatientCard[];
  alarms: DashboardAlarm[];
  generatedAt: string;
}
