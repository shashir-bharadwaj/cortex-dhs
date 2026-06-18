export interface ActiveInfusion {
  id: number;
  patientId: number;
  patientName?: string;
  bedLabel?: string;
  drugName: string;
  dose?: string;
  rateMlHr?: number;
  remainingVolMl?: number;
  estEndTime?: string;
  status: string;
}
