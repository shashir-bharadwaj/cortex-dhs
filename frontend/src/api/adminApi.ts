import api from "./client";
import type { AuditLog } from "../types/audit";
import type { DeviceType, DeviceTypePayload } from "../types/deviceType";
import type { Role, RolePayload } from "../types/role";

// ----------------------
// Audit Logs
// ----------------------

export async function getAuditLogs(): Promise<AuditLog[]> {
  const response = await api.get("/admin/audit-logs");
  return response.data;
}

// ----------------------
// Device Types
// ----------------------

export async function getDeviceTypes(): Promise<DeviceType[]> {
  const response = await api.get("/admin/device-types");
  return response.data;
}

export async function createDeviceType(payload: DeviceTypePayload) {
  const response = await api.post("/admin/device-types", payload);
  return response.data;
}

export async function updateDeviceType(
  id: number | string,
  payload: DeviceTypePayload
) {
  const response = await api.patch(`/admin/device-types/${id}`, payload);
  return response.data;
}

// ----------------------
// Roles & Permissions
// ----------------------

export async function getRoles(): Promise<Role[]> {
  const response = await api.get("/admin/roles");
  return response.data;
}

export async function getPermissions(): Promise<string[]> {
  const response = await api.get("/admin/permissions");
  return response.data;
}

export async function createRole(payload: RolePayload) {
  const response = await api.post("/admin/roles", payload);
  return response.data;
}

export async function updateRole(
  id: number | string,
  payload: RolePayload
) {
  const response = await api.patch(`/admin/roles/${id}`, payload);
  return response.data;
}