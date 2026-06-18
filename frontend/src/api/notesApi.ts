import api from "./client";

export interface ClinicalNote {
  id: number;
  patientId: number;
  authorId: number;
  authorName: string;
  noteType: "progress" | "nursing" | "order" | "handover";
  noteText: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateNotePayload {
  noteType: string;
  noteText: string;
}

export async function getPatientNotes(patientId: number): Promise<ClinicalNote[]> {
  const response = await api.get(`/patients/${patientId}/notes`);
  return response.data;
}

export async function createPatientNote(
  patientId: number,
  payload: CreateNotePayload,
): Promise<ClinicalNote> {
  const response = await api.post(`/patients/${patientId}/notes`, payload);
  return response.data;
}
