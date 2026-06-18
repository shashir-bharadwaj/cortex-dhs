import api from "./client";
import { Alert } from "../types/alert";

export async function getAlerts(params?: {
  severity?: string;
  acknowledged?: boolean;
  silenced?: boolean;
}): Promise<Alert[]> {
  const response = await api.get("/alarms", { params });
  return response.data;
}

export async function acknowledgeAlert(
  alarmId: number,
  acknowledgedBy: string
): Promise<Alert> {
  const response = await api.patch(`/alarms/${alarmId}/acknowledge`, {
    acknowledged_by: acknowledgedBy,
  });
  return response.data;
}
