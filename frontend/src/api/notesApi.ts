import api from "./client";
import type { TimelineEvent } from "../types/patientDetails";

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
export interface CreateTimelinePayload { 
  event:string;
  type:string;
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
export async function createPatientTimeline(
  patient_id: number,
  payload: CreateTimelinePayload
): Promise<TimelineEvent> {
  const response = await api.post(`/patients/${patient_id}/timeline`, payload);
  return response.data;
}

