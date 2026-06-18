import React, { useEffect, useState } from "react";
import { Table, Tag, message, Badge, Space, Button } from "antd";
import { CheckOutlined } from "@ant-design/icons";
import { getAlerts, acknowledgeAlert } from "../../api/alertsApi";
import { Alert } from "../../types/alert";
import PageHeader from "../../components/common/pageHeader";

const SEVERITY_COLOR: Record<string, string> = {
  Critical: "red",
  Warning: "orange",
};

const AlertsPage: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(false);

  async function fetchAlerts() {
    try {
      setLoading(true);
      const data = await getAlerts();
      setAlerts(data);
    } catch {
      message.error("Failed to load alerts");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchAlerts();
  }, []);

  async function handleAcknowledge(id: number) {
    try {
      await acknowledgeAlert(id, "current-user");
      await fetchAlerts();
      message.success("Alarm acknowledged");
    } catch {
      message.error("Failed to acknowledge alarm");
    }
  }

  const columns = [
    {
      title: "Bed",
      dataIndex: "bedId",
      key: "bedId",
      width: 80,
      render: (v: string) => <strong>{v}</strong>,
    },
    {
      title: "Patient",
      dataIndex: "patientName",
      key: "patientName",
    },
    {
      title: "Device",
      dataIndex: "device",
      key: "device",
    },
    {
      title: "Message",
      dataIndex: "message",
      key: "message",
    },
    {
      title: "Severity",
      dataIndex: "severity",
      key: "severity",
      render: (s: string) => (
        <Tag color={SEVERITY_COLOR[s] ?? "default"}>{s}</Tag>
      ),
    },
    {
      title: "Status",
      key: "status",
      render: (_: any, record: Alert) => (
        <Space>
          {record.acknowledged ? (
            <Tag color="green">Acknowledged</Tag>
          ) : (
            <Badge status="processing" text="Active" />
          )}
          {record.silenced && <Tag color="blue">Silenced</Tag>}
          {record.escalated && <Tag color="purple">Escalated</Tag>}
        </Space>
      ),
    },
    {
      title: "Action",
      key: "action",
      render: (_: any, record: Alert) =>
        !record.acknowledged ? (
          <Button
            size="small"
            icon={<CheckOutlined />}
            onClick={() => handleAcknowledge(record.id)}
          >
            Acknowledge
          </Button>
        ) : null,
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <PageHeader title="Alerts & Alarms" />

      <Table
        dataSource={alerts}
        rowKey="id"
        loading={loading}
        bordered
        columns={columns}
        rowClassName={(r: Alert) =>
          r.severity === "Critical" && !r.acknowledged ? "critical-alarm-row" : ""
        }
      />
    </div>
  );
};

export default AlertsPage;
