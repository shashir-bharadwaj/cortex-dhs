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
// Cloud Sync
// ----------------------

export interface HospitalSync {
  id: number;
  name: string;
  city: string;
  status: string;
  lastSync: string;
  data: string;
}

export interface CloudSummary {
  lastSync: string;
  dataSent: string;
  errors: number;
  hospitals: number;
}

export interface CloudSyncResponse {
  summary: CloudSummary;
  hospitals: HospitalSync[];
}

export async function getCloudSyncStatus(): Promise<CloudSyncResponse> {
  const response = await api.get("/admin/cloudsync");
  return response.data;
}

export async function triggerCloudSync(): Promise<{ started: boolean; message: string }> {
  const response = await api.post("/admin/cloudsync/trigger");
  return response.data;
}

// ----------------------
// Connectivity
// ----------------------

export interface ConnectivitySummary {
  online: number;
  offline: number;
  dataRate: string;
  latency: string;
}

export interface ConnectivityTimeline {
  time: string;
  online: number;
  offline: number;
}

export interface ConnectivityDevice {
  id: string;
  type: string;
  bed: string;
  status: string;
  lastSync: string;
  ip: string;
}

export interface ConnectivityResponse {
  summary: ConnectivitySummary;
  timeline: ConnectivityTimeline[];
  devices: ConnectivityDevice[];
}

export async function getConnectivityStatus(): Promise<ConnectivityResponse> {
  const response = await api.get("/admin/connectivity");
  return response.data;
}

// ----------------------
// Settings
// ----------------------

export interface SettingsPayload {
  hospitalName: string;
  adminEmail: string;
  settings: Record<string, boolean>;
}

export interface SettingsResponse extends SettingsPayload {}

export async function getSettings(): Promise<SettingsResponse> {
  const response = await api.get("/admin/settings");
  return response.data;
}

export async function saveSettings(payload: SettingsPayload): Promise<SettingsResponse> {
  const response = await api.post("/admin/settings", payload);
  return response.data;
}

// ----------------------
// Reports
// ----------------------

export interface ReportCardsResponse {
  title: string;
  desc: string;
}

export interface IcuDataResponse {
  name: string;
  value: number;
}

export interface AlertDataResponse {
  time: string;
  critical: number;
  warning: number;
  info: number;
}

export interface ReportsResponse {
  reportCards: ReportCardsResponse[];
  icuData: IcuDataResponse[];
  alertData: AlertDataResponse[];
}

export async function getReports(): Promise<ReportsResponse> {
  const response = await api.get("/admin/reports");
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