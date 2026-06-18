import api from "./client";
import { CreateNurseTaskPayload, NurseTask, NurseTaskSummary } from "../types/nurseTask";

export async function getNurseTasks(status?: string): Promise<NurseTaskSummary> {
  const params: Record<string, string> = {};
  if (status) params.task_status = status;
  const response = await api.get("/tasks/", { params });
  return response.data;
}

export async function createNurseTask(payload: CreateNurseTaskPayload): Promise<NurseTask> {
  const response = await api.post("/tasks/", payload);
  return response.data;
}

export async function completeNurseTask(taskId: number): Promise<NurseTask> {
  const response = await api.patch(`/tasks/${taskId}/complete`);
  return response.data;
}
