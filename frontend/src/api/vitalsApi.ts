import api from "./client";
import { Vital } from "../types/vital";

// export async function getVitals(): Promise<Vital[]> {
//   const response = await api.get("/vitals/");
//   return response.data;
// }

export async function getVitalsByPatient(patientId: number): Promise<Vital[]> {
  const response = await api.get(`/vitals/${patientId}`);
  return response.data;
}