export interface Patient {
  id: number;
  mrn?: string;
  crNumber?: string;
  name: string;
  contactNumber?: string;
  age?: number;
  gender?: string;
  bedId?: number;
  diagnosis?: string;
  weight?: number;
  height?: number;
  bsa?: number;
  bloodGroup?: string;
  doctor?: string;
  admissionTime?: string;
  hospitalId?: number;
  status: string;
  history: string[];
  comorbidities: string[];
}

export interface LatestVital {
  patientId?: number;
  bedId?: number;
  hr?: number;
  bpSys?: number;
  bpDia?: number;
  spo2?: number;
  temp?: number;
  rr?: number;
  status?: string;
  recordedAt?: string;
}
