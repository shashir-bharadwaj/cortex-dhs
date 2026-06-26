import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import LoginPage from "../pages/auth/LoginPage";
import DashboardPage from "../pages/dashboard/DashboardPage";
import PatientsPage from "../pages/patients/PatientsPage";
import PatientDetailPage from "../pages/patients/PatientDetailPage";
import DevicesPage from "../pages/devices/DevicesPage";
import AlertsPage from "../pages/alerts/AlertsPage";
import MedicationPage from "../pages/medication/MedicationPage";
import NotesPage from "../pages/notes/NotesPage";
import TasksPage from "../pages/tasks/TasksPage";
import HandoverPage from "../pages/handover/HandoverPage";

import UserManager from "../pages/admin/UserManager";
import RoleManager from "../pages/admin/RoleManager";
import DeviceTypeManager from "../pages/admin/DeviceTypeManager";
import AuditLogViewer from "../pages/admin/AuditLogViewer";

import ProtectedRoute from "../auth/ProtectedRoute";
import MainLayout from "../layouts/MainLayout";
import DashboardMain from "../pages/dashboard/MainDashboard";
import IcuManagement from "../pages/icu/IcuManagement";
import BedManagement from "../pages/bed/BedManagement";
import DeviceManagement from "../pages/devices/Devicemanagement";
import UsersAndRolesPage from "../pages/admin/UserRoleManagement";
import Settings from "../pages/Settings";

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
        <Route path="dashboard" element={<DashboardMain />} />
        <Route path="patients" element={<PatientsPage />} />
        <Route path="patients/:id" element={<PatientDetailPage />} />
        <Route path="devices" element={<DevicesPage />} />
        <Route path="alerts" element={<AlertsPage />} />
        <Route path="medication" element={<MedicationPage />} />
        <Route path="notes" element={<NotesPage />} />
        <Route path="tasks" element={<TasksPage />} />
        <Route path="handover" element={<HandoverPage />} />

        {/* Admin */}
        <Route path="admin/users" element={<UserManager />} />
        <Route path="admin/roles" element={<RoleManager />} />
        <Route path="admin/device-types" element={<DeviceTypeManager />} />
        <Route path="admin/audit-logs" element={<AuditLogViewer />} />
        <Route path="icumanagement" element={<IcuManagement />} />
        <Route path="bedmanagement" element={<BedManagement />} />
        <Route path="devicemanagement" element={<DeviceManagement />} />
        <Route path="usermanagement" element={<UsersAndRolesPage />} />
        <Route path="settings" element={<Settings />} />
      </Route>

      {/* Catch-all */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRouter;
