import api from "./client";
import type { Patient } from "../types/patient";
import type { Line } from "../types/line";
import type { AISuggestion } from "../types/ai";

export async function getPatients(): Promise<Patient[]> {
  const response = await api.get("/patients/");
  return response.data;
}

export async function getPatientById(id: number | string): Promise<Patient> {
  const response = await api.get(`/patients/${id}`);
  return response.data;
}

export async function createPatient(payload: Partial<Patient>) {
  const response = await api.post("/patients/", payload);
  return response.data;
}

export async function updatePatient(
  id: number | string,
  payload: Partial<Patient>
) {
  const response = await api.patch(`/patients/${id}`, payload);
  return response.data;
}

export async function deletePatient(id: number | string) {
  const response = await api.delete(`/patients/${id}`);
  return response.data;
}

// ----------------------
// Lines / Tubes
// ----------------------

export async function getPatientLines(id: number | string): Promise<Line[]> {
  const response = await api.get(`/patients/${id}/lines`);
  return response.data;
}

export interface CreateLinePayload {
  type: string;
  insertion_time: string;
  expected_removal_time?: string;
  notes?: string;
}

export async function createPatientLine(
  id: number | string,
  payload: CreateLinePayload
) {
  const response = await api.post(`/patients/${id}/lines`, payload);
  return response.data;
}

export async function markLineRemoved(lineId: number | string) {
  const response = await api.patch(`/lines/${lineId}`, {
    removed_time: new Date().toISOString(),
  });
  return response.data;
}

// ----------------------
// AI Suggestions
// ----------------------

export async function getPatientAiSuggestions(
  id: number | string
): Promise<AISuggestion> {
  const response = await api.get(`/patients/${id}/ai-suggestions`);
  return response.data;
}