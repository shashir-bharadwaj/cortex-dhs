export type TaskStatus = "pending" | "in_progress" | "completed";

export interface NurseTask {
  id: number;
  patientId: number;
  patientName: string;
  bedLabel: string;
  assignedToId?: number;
  title: string;
  description?: string;
  dueTime?: string;
  status: TaskStatus;
  createdAt?: string;
  completedAt?: string;
}

export interface NurseTaskSummary {
  total: number;
  pending: number;
  inProgress: number;
  completed: number;
  tasks: NurseTask[];
}

export interface CreateNurseTaskPayload {
  patientId: number;
  title: string;
  description?: string;
  dueTime?: string;
  assignedToId?: number;
}
