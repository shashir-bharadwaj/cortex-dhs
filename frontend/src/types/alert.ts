export interface Alert {
  id: number;
  patient_id: number;
  type: string;
  severity: string;
  message: string;
  created_at: string;
}