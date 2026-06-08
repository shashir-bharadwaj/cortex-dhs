export interface Device {
  id: number;
  bed_id: number;
  device_type_id?: number;
  device_type_name: string;
  serial_number?: string;
  status: string;
  last_seen: string;
}