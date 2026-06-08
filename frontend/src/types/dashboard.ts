export interface BedPatient {
  id: number;
  first_name: string;
  last_name: string;
}

export interface BedOverview {
  id: number;
  bed_number: string;
  status: "occupied" | "available";
  patient: BedPatient | null;
}