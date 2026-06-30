import React, { useEffect, useState } from "react";
import {
  Layout,
  Menu,
  Button,
  Badge,
  Avatar,
  Input,
  Dropdown,
  Space,
  Tooltip,
  message,
} from "antd";
import {
  DashboardOutlined,
  UserOutlined,
  AlertOutlined,
  MedicineBoxOutlined,
  FileTextOutlined,
  CheckSquareOutlined,
  SwapOutlined,
  LogoutOutlined,
  BellOutlined,
  SearchOutlined,
  ExclamationCircleFilled,
  MenuOutlined,
  DownOutlined,
} from "@ant-design/icons";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { getAlerts, acknowledgeAlert } from "../api/alertsApi";
import { Alert } from "../types/alert";
import "./MainLayout.css";
import { Bed, Server, Settings, Users } from "lucide-react";

const { Sider, Content, Header } = Layout;

const SIDER_EXPANDED = 200;
// Matches AntD's inline-collapsed menu width so icons don't clip.
const SIDER_COLLAPSED = 76;

const BRAND_PURPLE = "#5b2be0";

function currentShiftLabel(): string {
  const hour = new Date().getHours();
  if (hour >= 7 && hour < 15) return "Morning (7AM–3PM)";
  if (hour >= 15 && hour < 23) return "Evening (3PM–11PM)";
  return "Night (11PM–7AM)";
}

/** Heartbeat / ECG activity line — brand mark */
const EcgIcon: React.FC<{ size?: number; color?: string }> = ({
  size = 22,
  color = "#1a1a2e",
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke={color}
    strokeWidth={2.2}
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
  </svg>
);

/** Lucide-style "log out" glyph (box open on the right + arrow). */
const LogoutIcon: React.FC<{ size?: number; color?: string }> = ({
  size = 16,
  color = "#dc2626",
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke={color}
    strokeWidth={2}
    strokeLinecap="round"
    strokeLinejoin="round"
    style={{ display: "block" }}
  >
    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
    <polyline points="16 17 21 12 16 7" />
    <line x1="21" y1="12" x2="9" y2="12" />
  </svg>
);

const MainLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout, user } = useAuth();
  const [alarms, setAlarms] = useState<Alert[]>([]);
  const [criticalAlarms, setCriticalAlarms] = useState<Alert[]>([]);
  const [collapsed, setCollapsed] = useState(false);

  async function fetchAlarms() {
    try {
      const data = await getAlerts({ acknowledged: false });
      setAlarms(data);
      setCriticalAlarms(data.filter((a) => a.severity === "Critical"));
    } catch {
      // non-blocking
    }
  }

  useEffect(() => {
    fetchAlarms();
    const interval = setInterval(fetchAlarms, 30_000);
    return () => clearInterval(interval);
  }, []);

  const hasCritical = alarms.some((a) => a.severity === "Critical");
  const isAlertsActive = location.pathname.startsWith("/alerts");

  const userRole = (localStorage.getItem("role") || "").toLowerCase();

  const navItems = [
    { key: "/dashboard", icon: <DashboardOutlined />, label: "Dashboard", roles: ["nurse", "admin"] },
    { key: "/patients", icon: <UserOutlined />, label: "Patients", roles: ["nurse"] },
    {
      key: "/alerts",
      icon: collapsed ? (
        <Badge
          count={alarms.length}
          size="small"
          overflowCount={99}
          style={{ background: hasCritical ? "#ff4d4f" : "#fa8c16" }}
          offset={[2, -4]}
        >
          <AlertOutlined style={{ fontSize: 16 }} />
        </Badge>
      ) : (
        <AlertOutlined />
      ),
      roles: ["nurse"],
      label: (
        <span
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            width: "100%",
          }}
        >
          <span>Alerts</span>
          {alarms.length > 0 && (
            <span
              style={{
                // On the purple selected bar use a dark contrast badge
                // (matches mockup); otherwise red/orange by severity.
                background: isAlertsActive
                  ? "rgba(0,0,0,0.28)"
                  : hasCritical
                    ? "#ff4d4f"
                    : "#fa8c16",
                color: "#fff",
                fontSize: 11,
                fontWeight: 700,
                minWidth: 22,
                height: 22,
                lineHeight: "22px",
                textAlign: "center",
                borderRadius: 11,
                padding: "0 6px",
              }}
            >
              {alarms.length}
            </span>
          )}
        </span>
      ),
    },
    { key: "/medication", icon: <MedicineBoxOutlined />, label: "Medication", roles: ["nurse"] },
    { key: "/notes", icon: <FileTextOutlined />, label: "Notes", roles: ["nurse"] },
    { key: "/tasks", icon: <CheckSquareOutlined />, label: "Tasks", roles: ["nurse"] },
    { key: "/handover", icon: <SwapOutlined />, label: "Handover", roles: ["nurse"] },
    { key: "/icumanagement", icon: <Server />, label: "ICU Management", roles: ["admin"] },
    { key: "/bedmanagement", icon: <Bed />, label: "Bed Management", roles: ["admin"] },
    { key: "/devicemanagement", icon: <Settings />, label: "Device Management", roles: ["admin"] },
      { key: "/connectivity", icon: <Settings />, label: "Connectivity", roles: ["admin"] },
    { key: "/usermanagement", icon: <Users />, label: "User Management", roles: ["admin"] },
     { key: "/cloudsync", icon: <Users />, label: "Cloud Sync", roles: ["admin"] },
      { key: "/audit", icon: <Users />, label: "Audit", roles: ["admin"] },
       { key: "/reports", icon: <Users />, label: "Reports", roles: ["admin"] },
     { key: "/settings", icon: <Settings />, label: "Settings", roles: ["admin"] },
  ];

  const menuItems = navItems.filter((item) => userRole && item.roles.includes(userRole));

  function handleLogout() {
    logout();
    navigate("/login");
  }

  async function handleAcknowledge() {
    const target = criticalAlarms[0];
    if (!target) return;
    try {
      const name = user ? `${user.firstName} ${user.lastName}` : "Staff";
      await acknowledgeAlert(target.id, name);
      message.success("Alert acknowledged");
      fetchAlarms();
    } catch {
      message.error("Could not acknowledge alert");
    }
  }

  const selectedKey =
    menuItems.find((item) =>
      location.pathname === item.key || location.pathname.startsWith(`${item.key}/`)
    )?.key ?? "/dashboard";

  const userDisplayName = user ? `${user.firstName} ${user.lastName}` : "User";
  const firstCritical = criticalAlarms[0];
  const siderWidth = collapsed ? SIDER_COLLAPSED : SIDER_EXPANDED;

  const userMenuItems = [
    {
      key: "logout",
      icon: <LogoutOutlined />,
      label: "Logout",
      onClick: handleLogout,
    },
  ];

  return (
    <Layout style={{ minHeight: "100vh" }}>
      {/* ---------------- Sidebar (light theme) ---------------- */}
      <Sider
        width={SIDER_EXPANDED}
        collapsedWidth={SIDER_COLLAPSED}
        collapsed={collapsed}
        theme="light"
        style={{
          background: "#ffffff",
          borderRight: "1px solid #ececf1",
          position: "fixed",
          height: "100vh",
          left: 0,
          top: 0,
          zIndex: 100,
          overflow: "hidden",
          transition: "width 0.2s",
        }}
      >
        {/* Logo row with collapse toggle */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: collapsed ? "center" : "space-between",
            padding: collapsed ? "12px 0" : "14px 8px",
            minHeight: 56,
          }}
        >
          {!collapsed ? (
            <>
              <div style={{ display: "flex", alignItems: "center", gap: 9 }}>
                <EcgIcon size={20} color="#1a1a2e" />
                <span
                  style={{
                    color: "#1a1a2e",
                    fontWeight: 800,
                    fontSize: 14,
                    letterSpacing: 0.5,
                    whiteSpace: "nowrap",
                  }}
                >
                  BPL CORTEX
                </span>
              </div>
              <Button
                type="text"
                icon={
                  <MenuOutlined style={{ color: "#6b6b80", fontSize: 16 }} />
                }
                onClick={() => setCollapsed(true)}
                style={{ padding: 0, height: "auto", minWidth: 28 }}
              />
            </>
          ) : (
            <Button
              type="text"
              icon={<MenuOutlined style={{ color: "#6b6b80", fontSize: 18 }} />}
              onClick={() => setCollapsed(false)}
              style={{ padding: 0, height: "auto", minWidth: 32 }}
            />
          )}
        </div>

        {/* Active Unit section */}
        {!collapsed && (
          <div
            style={{
              padding: "4px 18px 16px",
              borderBottom: "1px solid #ececf1",
            }}
          >
            <div
              style={{
                color: "#9a9aae",
                fontSize: 10.5,
                fontWeight: 600,
                letterSpacing: 0.8,
                marginBottom: 4,
              }}
            >
              ACTIVE UNIT
            </div>
            <div style={{ color: "#1a1a2e", fontSize: 13, fontWeight: 700 }}>
              {user?.unitId ? `ICU Unit ${user.unitId}` : "Cardiac ICU"}
            </div>
            <div style={{ color: "#9a9aae", fontSize: 11, marginTop: 2 }}>
              {currentShiftLabel()}
            </div>
          </div>
        )}

        {/* Navigation menu */}
        <Menu
          className="cortex-sider-menu"
          theme="light"
          mode="inline"
          selectedKeys={[selectedKey]}
          inlineCollapsed={collapsed}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{ border: "none", marginTop: 8, fontSize: 13 }}
        />

        {/* Logout (red, bottom) */}
        <div
          style={{
            position: "absolute",
            bottom: 0,
            left: 0,
            right: 0,
            padding: collapsed ? "8px 0 18px" : "8px 18px 18px",
            display: "flex",
            justifyContent: collapsed ? "center" : "flex-start",
            background: "#ffffff",
          }}
        >
          {collapsed ? (
            <Tooltip title="Logout" placement="right">
              <Button
                type="text"
                icon={<LogoutIcon size={18} />}
                onClick={handleLogout}
                style={{
                  padding: 0,
                  height: 40,
                  width: 40,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              />
            </Tooltip>
          ) : (
            <Button
              type="text"
              icon={<LogoutIcon size={16} />}
              onClick={handleLogout}
              style={{
                color: "#dc2626",
                fontWeight: 600,
                padding: 0,
                height: "auto",
                display: "flex",
                alignItems: "center",
                gap: 8,
              }}
            >
              Logout
            </Button>
          )}
        </div>
      </Sider>

      {/* ---------------- Main content ---------------- */}
      <Layout
        style={{
          marginLeft: siderWidth,
          transition: "margin-left 0.2s",
          minHeight: "100vh",
        }}
      >
        {/* Top header */}
        <div style={{ position: "sticky", top: 0, zIndex: 99 }}>
          <Header
            style={{ background: "#fff", padding: "0 24px", display: "flex", alignItems: "center", gap: 16, borderBottom: "1px solid #ececf1", height: 60, lineHeight: "normal" }}>
            <Input
              prefix={<SearchOutlined style={{ color: "#bbb" }} />}
              placeholder="Search patient, bed…"
              style={{
                maxWidth: 360,
                borderRadius: 22,
                background: "#f5f6fa",
                border: "none",
              }}
            />

            <div style={{ flex: 1 }} />

            <Space size={20} align="center">
              {/* Hospital selector pill */}
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  height: 38,
                  lineHeight: 1,
                  background: "#f4f0fe",
                  border: "1px solid #e7defb",
                  borderRadius: 19,
                  padding: "0 16px",
                  cursor: "pointer",
                }}
              >
                <EcgIcon size={16} color={BRAND_PURPLE} />
                <span
                  style={{ color: BRAND_PURPLE, fontWeight: 600, fontSize: 13 }}
                >
                  City General Hospital
                </span>
                <DownOutlined style={{ color: BRAND_PURPLE, fontSize: 10 }} />
              </div>

              <Tooltip title="Active Alarms">
                <Badge count={alarms.length} size="small" overflowCount={99}>
                  <Button
                    type="text"
                    icon={<BellOutlined style={{ fontSize: 18 }} />}
                    style={{ padding: "0 4px" }}
                    onClick={() => navigate("/alerts")}
                  />
                </Badge>
              </Tooltip>

              <Dropdown
                menu={{ items: userMenuItems }}
                placement="bottomRight"
                trigger={["click"]}
              >
                <Space style={{ cursor: "pointer" }}>
                  <div style={{ lineHeight: 1.2, textAlign: "right" }}>
                    <div
                      style={{ fontSize: 13, fontWeight: 600, color: "#1a1a2e" }}
                    >
                      {user?.shift ? "Nurse" : userDisplayName}
                    </div>
                    <div style={{ fontSize: 11, color: "#888" }}>
                      City General Hospital
                    </div>
                  </div>
                  <Avatar
                    size={34}
                    style={{ background: "#f0eaff", color: BRAND_PURPLE }}
                    icon={<UserOutlined />}
                  />
                </Space>
              </Dropdown>
            </Space>
          </Header>

          {/* Critical alarm banner (below header, inside content area) */}
          {firstCritical && (
            <div
              style={{
                background: "#e60023",
                color: "#fff",
                padding: "5px 18px",
                display: "flex",
                alignItems: "center",
                gap: 8,
                fontSize: 12,
              }}
            >
              <ExclamationCircleFilled style={{ fontSize: 9 }} />
              <span style={{ fontWeight: 700, letterSpacing: 0.3 }}>
                CRITICAL ALERT
              </span>
              <span>
                {firstCritical.bedId} – {firstCritical.message}
              </span>
              {criticalAlarms.length > 1 && (
                <span style={{ opacity: 0.85, fontWeight: 600 }}>
                  +{criticalAlarms.length - 1} more
                </span>
              )}
              <div style={{ flex: 1 }} />
              <Button
                size="small"
                onClick={handleAcknowledge}
                style={{ background: "rgba(255,255,255,0.18)", border: "1px solid rgba(255,255,255,0.5)", color: "#fff", fontWeight: 600, borderRadius: 5, height: 24, fontSize: 11 }}
              >
                Acknowledge
              </Button>
              <Button
                size="small"
                onClick={() => navigate("/alerts")}
                style={{ background: "rgba(255,255,255,0.18)", border: "1px solid rgba(255,255,255,0.5)", color: "#fff", fontWeight: 600, borderRadius: 5, height: 24, fontSize: 11 }}
              >
                View Alerts
              </Button>
            </div>
          )}
        </div>
        <Content style={{ background: "#f5f6fa" }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
