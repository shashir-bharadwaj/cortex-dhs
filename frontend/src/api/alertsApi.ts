import api from "./client";
import { Alert } from "../types/alert";

export async function getAlerts(): Promise<Alert[]> {
  const response = await api.get("/alerts/");
  return response.data;
}

// export async function getAlertsByPatient(patientId: number): Promise<Alert[]> {
//   const response = await api.get(`/alerts/?patient_id=${patientId}`);
//   return response.data;
// }