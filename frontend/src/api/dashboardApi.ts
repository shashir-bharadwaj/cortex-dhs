import api from "./client";
import { DashboardOverview, ICUUnitMaster } from "../types/dashboard";

export async function getDashboardUnits(): Promise<ICUUnitMaster[]> {
  const response = await api.get("/dashboard/units");
  return response.data;
}

export async function getDashboardOverview(unitId: number): Promise<DashboardOverview> {
  const response = await api.get("/dashboard/overview", {
    params: { unitId },
  });
  return response.data;
}
