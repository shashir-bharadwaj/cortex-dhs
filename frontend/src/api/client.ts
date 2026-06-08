import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  console.log("API REQUEST:", {
    method: config.method,
    url: `${config.baseURL}${config.url}`,
    data: config.data,
    headers: config.headers,
  });

  return config;
});

api.interceptors.response.use(
  (response) => {
    console.log("API RESPONSE:", response.status, response.config.url, response.data);
    return response;
  },
  (error) => {
    console.error("API ERROR:", {
      status: error?.response?.status,
      url: error?.config?.url,
      data: error?.response?.data,
    });
    return Promise.reject(error);
  }
);

export default api;