export interface Vital {
  id: number;
  patient_id: number;
  heart_rate?: number;
  spo2?: number;
  blood_pressure?: string;
  recorded_at: string;
}