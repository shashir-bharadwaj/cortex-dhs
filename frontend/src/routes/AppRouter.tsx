import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import LoginPage from "../pages/auth/LoginPage";
import DashboardPage from "../pages/dashboard/DashboardPage";
import PatientsPage from "../pages/patients/PatientsPage";
import PatientDetailPage from "../pages/patients/PatientDetailPage";
import DevicesPage from "../pages/devices/DevicesPage";

import UserManager from "../pages/admin/UserManager";
import RoleManager from "../pages/admin/RoleManager";
import DeviceTypeManager from "../pages/admin/DeviceTypeManager";
import AuditLogViewer from "../pages/admin/AuditLogViewer";

import ProtectedRoute from "../auth/ProtectedRoute";
import MainLayout from "../layouts/MainLayout";

const AppRouter: React.FC = () => {
  return (
    <Routes>
      {/* Public Route */}
      <Route path="/login" element={<LoginPage />} />

      {/* Protected App Routes */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="patients" element={<PatientsPage />} />
        <Route path="patients/:id" element={<PatientDetailPage />} />
        <Route path="devices" element={<DevicesPage />} />

        {/* Admin */}
        <Route path="admin/users" element={<UserManager />} />
        <Route path="admin/roles" element={<RoleManager />} />
        <Route path="admin/device-types" element={<DeviceTypeManager />} />
        <Route path="admin/audit-logs" element={<AuditLogViewer />} />
      </Route>

      {/* Catch-all */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRouter;