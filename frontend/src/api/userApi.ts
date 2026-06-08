import api from "./client";
import { User, CreateUserPayload } from "../types/user";

export async function getUsers(): Promise<User[]> {
  const response = await api.get("/users/");
  return response.data;
}

export async function getUserById(id: number): Promise<User> {
  const response = await api.get(`/users/${id}`);
  return response.data;
}

export async function createUser(payload: CreateUserPayload) {
  const response = await api.post("/users/", payload);
  return response.data;
}