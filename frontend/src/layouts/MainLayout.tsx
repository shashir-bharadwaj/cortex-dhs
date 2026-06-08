import React from "react";
import { Layout, Menu, Button, Typography } from "antd";
import {
  DashboardOutlined,
  UserOutlined,
  MedicineBoxOutlined,
  DesktopOutlined,
  TeamOutlined,
  SafetyOutlined,
  SettingOutlined,
  FileTextOutlined,
  LogoutOutlined,
} from "@ant-design/icons";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

const { Header, Sider, Content } = Layout;
const { Title } = Typography;

const MainLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout } = useAuth();

  const menuItems = [
    {
      key: "/dashboard",
      icon: <DashboardOutlined />,
      label: "Dashboard",
    },
    {
      key: "/patients",
      icon: <UserOutlined />,
      label: "Patients",
    },
    {
      key: "/devices",
      icon: <DesktopOutlined />,
      label: "Devices",
    },
    {
      key: "/admin/users",
      icon: <TeamOutlined />,
      label: "Users",
    },
    {
      key: "/admin/roles",
      icon: <SafetyOutlined />,
      label: "Roles",
    },
    {
      key: "/admin/device-types",
      icon: <SettingOutlined />,
      label: "Device Types",
    },
    {
      key: "/admin/audit-logs",
      icon: <FileTextOutlined />,
      label: "Audit Logs",
    },
  ];

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider width={240}>
        <div style={{ padding: "16px", color: "white" }}>
          <Title level={4} style={{ color: "white", margin: 0 }}>
            ICU Monitor
          </Title>
        </div>

        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>

      <Layout>
        <Header
          style={{
            background: "#fff",
            padding: "0 24px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            borderBottom: "1px solid #f0f0f0",
          }}
        >
          <Title level={4} style={{ margin: 0 }}>
            ICU Clinical Dashboard
          </Title>

          <Button icon={<LogoutOutlined />} onClick={handleLogout}>
            Logout
          </Button>
        </Header>

        <Content style={{ margin: "24px", background: "#fff", padding: 24 }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;