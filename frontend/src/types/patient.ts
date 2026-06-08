export interface Patient {
  id: number;
  first_name: string;
  last_name: string;
  bed_id: number;
  admission_time: string;
  date_of_birth?: string;
  gender?: string;
}