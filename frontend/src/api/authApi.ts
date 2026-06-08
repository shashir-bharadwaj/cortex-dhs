import api from "./client";

export interface LoginResponse {
  access_token: string;
  refresh_token?: string;
  token_type: string;
  mfa_required?: boolean;
}

export async function loginApi(
  username: string,
  password: string
): Promise<LoginResponse> {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const response = await api.post("api/v1/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  return response.data;
}