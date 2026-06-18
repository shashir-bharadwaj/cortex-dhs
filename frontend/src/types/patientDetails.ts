import type { Patient, LatestVital } from "./patient";
import type { Alert } from "./alert";

export interface Vital {
  id: number;
  patientId: number;
  hr?: number;
  bpSys?: number;
  bpDia?: number;
  spo2?: number;
  temp?: number;
  rr?: number;
  recordedAt?: string;
}

export interface StaffAssignment {
  staffName?: string;
  staffRole?: string;
  assignmentType: string;
}

/** DeviceMasterResponse is serialized in snake_case (no field aliases). */
export interface DeviceMaster {
  id: number;
  device_type: string;
  manufacturer: string;
  model: string;
  serial: string;
  bed_id?: number | null;
  ip_address: string;
  status: string;
}

export interface TimelineEvent {
  id: number;
  time?: string;
  event: string;
  type: string;
}

export interface ClinicalNote {
  id: number;
  patientId: number;
  authorId: number;
  authorName: string;
  noteType: string;
  noteText: string;
  createdAt: string;
  updatedAt: string;
}

export interface VentilatorParams {
  id: number;
  patientId: number;
  mode?: string;
  fio2?: number;
  peep?: number;
  setRr?: number;
  tidalVolume?: number;
  recordedAt?: string;
}

export interface LabData {
  id: number;
  patientId: number;
  ph?: number;
  pao2?: number;
  paco2?: number;
  hco3?: number;
  rbs?: number;
  recordedAt?: string;
}

export interface FluidBalance {
  patientId: number;
  date: string;
  inMl: number;
  outMl: number;
  balanceMl: number;
}

export type MedicationOrderType = "PRN" | "STAT" | "Infusion";
export type MedicationStatus =
  | "Pending"
  | "Running"
  | "Given"
  | "Completed"
  | "Cancelled";

export interface MedicationOrder {
  id: number;
  patientId: number;
  drugName: string;
  orderType: MedicationOrderType;
  dose?: string;
  route?: string;
  schedule?: string;
  status: MedicationStatus;
  rateMlHr?: number;
  remainingVolMl?: number;
  estEndTime?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface PatientOverview {
  patient: Patient;
  latestVitals?: LatestVital | null;
  activeAlarmCount: number;
  deviceCount: number;
  unitId?: number | null;
}

export interface PatientDetails {
  overview: PatientOverview;
  staffAssignment: StaffAssignment[];
  vitals: Vital[];
  devices: DeviceMaster[];
  alarms: Alert[];
  timeline: TimelineEvent[];
  notes: ClinicalNote[];
  medications: MedicationOrder[];
  ventilatorParams?: VentilatorParams | null;
  labData?: LabData | null;
  fluidBalance?: FluidBalance | null;
  reports: unknown[];
}
