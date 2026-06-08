export interface User {
  id: number;
  username: string;
  full_name: string;
  email: string;
  role_id: number;
  role?: string;
}

export interface CreateUserPayload {
  username: string;
  full_name: string;
  email: string;
  password: string;
  role_id: number;
}

export interface RoleOption {
  id: number;
  name: string;
}