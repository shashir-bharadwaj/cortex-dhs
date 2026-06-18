import api from "./client";
import type { Patient } from "../types/patient";
import type { Line } from "../types/line";
import type { AISuggestion } from "../types/ai";
import type { Flowsheet } from "../types/flowsheet";
import type { PatientDetails } from "../types/patientDetails";

export async function getPatients(params?: {
  limit?: number;
  offset?: number;
}): Promise<Patient[]> {
  const response = await api.get("/patients/", { params });
  return response.data;
}

/** Paged variant that also returns the total count (from X-Total-Count). */
export async function getPatientsPaged(params: {
  limit: number;
  offset: number;
}): Promise<{ items: Patient[]; total: number }> {
  const response = await api.get("/patients/", { params });
  const header = response.headers["x-total-count"];
  const total = header != null ? Number(header) : response.data.length;
  return { items: response.data, total };
}

export async function getPatientById(id: number | string): Promise<Patient> {
  const response = await api.get(`/patients/${id}`);
  return response.data;
}

export async function getPatientDetails(
  id: number | string
): Promise<PatientDetails> {
  const response = await api.get(`/patients/${id}/details`);
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
  const response = await api.put(`/patients/${id}`, payload);
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

// ----------------------
// Flowsheet
// ----------------------

export async function getPatientFlowsheet(
  id: number | string,
  date?: string
): Promise<Flowsheet> {
  const params = date ? { date } : {};
  const response = await api.get(`/patients/${id}/flowsheet`, { params });
  return response.data;
}

// ----------------------
// Reports
// ----------------------

export async function getDailySummaryReport(
  id: number | string
): Promise<Record<string, unknown>> {
  const response = await api.get(`/patients/${id}/reports/daily-summary`);
  return response.data;
}

export async function getDischargeSummaryReport(
  id: number | string
): Promise<Record<string, unknown>> {
  const response = await api.get(`/patients/${id}/reports/discharge-summary`);
  return response.data;
}

/** Downloads today's vitals as a CSV file via the browser. */
export async function downloadVitalsCsv(id: number | string): Promise<void> {
  const response = await api.get(`/patients/${id}/reports/vitals-csv`, {
    responseType: "blob",
  });
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `vitals_patient_${id}.csv`);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}