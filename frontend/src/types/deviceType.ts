export interface DeviceType {
  id: number;
  name: string;
  company: string;
  output_spec?: string;
  adapter_name?: string;
  created_at: string;
  updated_at: string;
}

export interface DeviceTypePayload {
  name: string;
  company: string;
  output_spec?: string;
  adapter_name?: string;
}