export interface Role {
  id: number;
  name: string;
  description?: string;
  permissions: string[];
}

export interface RolePayload {
  name: string;
  description?: string;
  permission_names: string[];
}