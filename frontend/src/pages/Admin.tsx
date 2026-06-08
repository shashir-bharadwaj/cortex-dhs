import React from 'react';
import { Tabs } from 'antd';
import DeviceTypeManager from './admin/DeviceTypeManager';
import UserManager from './admin/UserManager';
import RoleManager from './admin/RoleManager';
import AuditLogViewer from './admin/AuditLogViewer';

const AdminPage: React.FC = () => {
  const items = [
    {
      key: 'device-types',
      label: 'Device Types',
      children: <DeviceTypeManager />,
    },
    {
      key: 'users',
      label: 'Users',
      children: <UserManager />,
    },
    {
      key: 'roles',
      label: 'Roles',
      children: <RoleManager />,
    },
    {
      key: 'audit-logs',
      label: 'Audit Logs',
      children: <AuditLogViewer />,
    },
  ];
  return (
    <Tabs defaultActiveKey="device-types" items={items} />
  );
};

export default AdminPage;