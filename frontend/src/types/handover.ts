export interface HandoverVitals {
  hr?: number;
  spo2?: number;
  bp?: string;
  rr?: number;
  temp?: number;
}

export interface HandoverNote {
  text: string;
  author: string;
}

export interface HandoverPatientCard {
  patientId: number;
  bedLabel: string;
  patientName: string;
  age?: number;
  gender?: string;
  diagnosis?: string;
  vitals: HandoverVitals;
  doctor?: string;
  unacknowledgedAlarms: number;
  pendingTasks: number;
  latestNote?: HandoverNote;
  ventilatorActive: boolean;
}

export interface ShiftInfo {
  name: string;
  start: string;
  end: string;
}

export interface ShiftHandoverSummary {
  shift: ShiftInfo;
  patients: HandoverPatientCard[];
}
