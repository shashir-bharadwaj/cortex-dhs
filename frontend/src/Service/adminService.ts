import api from "./api";
//ICU
export const getICU = async () => {
  const response = await api.get(`/admin/icu-units`);
  return response.data;
};
export const addICU = async (form: any) => {
  const response = await api.post(`/admin/icu-units`,form);
  return response.data;
};
export const updateICU = async (id:number,form: any) => {
  const response = await api.put(`/admin/icu-units/${id}`,form);
  return response.data;
};
export const deleteData = async (id:number,module:string) => {
  const response = await api.delete(`/admin/${module}/${id}`);
  return response.data;
};
//BED
export const getBeds = async () => {
  const response = await api.get(`/admin/beds`);
  return response.data;
};
export const addBed = async (form: any) => {
  const response = await api.post(`/admin/beds`,form);
  return response.data;
};
export const updateBed = async (id:number,form: any) => {
  const response = await api.put(`/admin/beds/${id}`,form);
  return response.data;
};
//Devices
export const getDevices = async () => {
  const response = await api.get(`/admin/devices`);
  return response.data;
};
export const addDevice = async (form: any) => {
  const response = await api.post(`/admin/devices`,form);
  return response.data;
};
export const updateDevice = async (id:number,form: any) => {
  const response = await api.put(`/admin/devices/${id}`,form);
  return response.data;
};
export const deleteDevice = async (id:number,module:string) => {
  const response = await api.delete(`/admin/${module}/${id}`);
  return response.data;
};
//User
export const getUsers = async () => {
  const response = await api.get(`/admin/users`);
  return response.data;
};
export const addUser = async (form: any) => {
  const response = await api.post(`/admin/users`,form);
  return response.data;
};
export const updateUser = async (id:number,form: any) => {
  const response = await api.put(`/admin/users/${id}`,form);
  return response.data;
};
//Roles
export const getRolePermission = async () => {
  const response = await api.get(`/admin/users/permissions`);
  return response.data;
};
export const updateRolePermission = async (id:number,form: any) => {
  const response = await api.put(`/admin/users/roles/${id}/permissions`,form);
  return response.data;
};
export const createRolePermission = async (form: any) => {
  const response = await api.post(`/admin/users/roles`,form);
  return response.data;
};