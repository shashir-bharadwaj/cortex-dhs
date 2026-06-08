export interface Line {
  id: number;
  patient_id: number;
  type: string;
  insertion_time: string;
  expected_removal_time?: string | null;
  removed_time?: string | null;
  status: string;
  notes?: string;
}