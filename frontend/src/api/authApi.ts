import api from "./client";

export interface AuthUser {
  id: number;
  userId: string;
  firstName: string;
  lastName: string;
  email: string;
  roleId: number;
  hospitalId: number;
  unitId: number;
  shift: string;
  isActive: boolean;
}

export interface LoginResponse {
  token: string;
  user: AuthUser;
}

export async function loginApi(email: string, password: string): Promise<LoginResponse> {
  const response = await api.post("/auth/login", { email, password });
  return response.data;
}
