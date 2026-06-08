import api from "./client";
import type { Device } from "../types/device";

export async function getDevices(): Promise<Device[]> {
  const response = await api.get("/devices/");
  return response.data;
}

export async function getDeviceById(id: number | string): Promise<Device> {
  const response = await api.get(`/devices/${id}`);
  return response.data;
}