import React, { useState } from "react";
import { Card, Typography, Input, Switch, Divider, Button, message } from "antd";
import { SaveOutlined } from "@ant-design/icons";

const { Title, Text } = Typography;

const SystemSettingsPage = () => {
  const [hospitalName, setHospitalName] = useState("Metro General Hospital");
  const [adminEmail, setAdminEmail] = useState("admin@metrogeneral.com");

  const [settings, setSettings] = useState({
    realTimeAlerts: true,
    autoSync: true,
    autoDiscovery: false,
  });

  const handleToggle = (key: string, value: boolean) => {
    setSettings((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const handleSave = () => {
    console.log({ hospitalName, adminEmail, settings });
    message.success("Settings saved successfully!");
  };

  const styles = {
    page: { padding: 24 },
    header: { marginBottom: 20 },
    card: { marginBottom: 20, borderRadius: 12 },
    cardSection: { marginTop: 16 },
    row: { display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 16 },
    input: { marginTop: 8 },
    saveButton: {
      marginTop: 24,
      background: "#2aa198",
      color: "#fff",
      border: "none",
      borderRadius: 8,
      padding: "0 20px",
      height: 44,
      fontWeight: 500,
    },
  };

  return (
      <div style={styles.page}>
        <div style={styles.header}>
          <Title level={3}>System Settings</Title>
          <Text type="secondary">Configure platform settings and preferences</Text>
        </div>

        <Card style={styles.card}>
          <Title level={5}>General</Title>

          <div style={styles.cardSection}>
            <Text strong>Hospital Name</Text>
            <Input value={hospitalName} onChange={(e) => setHospitalName(e.target.value)} style={styles.input} />
          </div>

          <div style={styles.cardSection}>
            <Text strong>Admin Email</Text>
            <Input value={adminEmail} onChange={(e) => setAdminEmail(e.target.value)} style={styles.input} />
          </div>
        </Card>

        <Card style={{ borderRadius: 12 }}>
          <Title level={5}>Monitoring</Title>

          <div style={styles.row}>
            <div>
              <Text strong>Real-time Alerts</Text>
              <br />
              <Text type="secondary">Receive instant push notifications</Text>
            </div>
            <Switch checked={settings.realTimeAlerts} onChange={(val) => handleToggle("realTimeAlerts", val)} />
          </div>

          <Divider />

          <div style={styles.row}>
            <div>
              <Text strong>Auto-sync to Cloud</Text>
              <br />
              <Text type="secondary">Automatically sync data every 5 minutes</Text>
            </div>
            <Switch checked={settings.autoSync} onChange={(val) => handleToggle("autoSync", val)} />
          </div>

          <Divider />

          <div style={styles.row}>
            <div>
              <Text strong>Device Auto-discovery</Text>
              <br />
              <Text type="secondary">Automatically detect new devices on network</Text>
            </div>
            <Switch checked={settings.autoDiscovery} onChange={(val) => handleToggle("autoDiscovery", val)} />
          </div>
        </Card>

        <div style={styles.saveButton}>
          <Button icon={<SaveOutlined />} size="large" onClick={handleSave} style={{ background: "#2aa198", color: "#fff", border: "none", borderRadius: 8, padding: "0 20px", height: 44, fontWeight: 500 }}>
            Save Settings
          </Button>
        </div>
      </div>
  );
};

export default SystemSettingsPage;
