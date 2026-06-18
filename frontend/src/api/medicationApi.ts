import api from "./client";
import { ActiveInfusion } from "../types/activeInfusion";

export async function getActiveInfusions(): Promise<ActiveInfusion[]> {
  const response = await api.get("/medications/active-infusions");
  return response.data;
}
