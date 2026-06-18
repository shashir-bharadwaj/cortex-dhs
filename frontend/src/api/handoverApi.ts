import api from "./client";
import { ShiftHandoverSummary } from "../types/handover";

export async function getShiftHandoverSummary(): Promise<ShiftHandoverSummary> {
  const response = await api.get("/handover/shift-summary");
  return response.data;
}
