export interface FlowsheetRow {
  parameter: string;
  values: Record<string, number | string | null>;
}

export interface Flowsheet {
  patientId: number;
  date: string;
  hours: number[];
  rows: FlowsheetRow[];
}
