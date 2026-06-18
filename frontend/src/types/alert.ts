export interface Alert {
  id: number;
  patientId: number;
  patientName: string;
  bedId: string;
  device: string;
  message: string;
  severity: "Warning" | "Critical";
  acknowledged: boolean;
  silenced: boolean;
  escalated: boolean;
  timestamp: string;
  acknowledgedBy?: string | null;
  silencedBy?: string | null;
  escalatedBy?: string | null;
  escalateTo?: string | null;
}
