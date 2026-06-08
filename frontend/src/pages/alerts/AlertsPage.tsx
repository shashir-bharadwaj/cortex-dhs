import React, { useEffect, useState } from "react";
import { Table, message, Tag } from "antd";
import { getAlerts } from "../../api/alertsApi";
import { Alert } from "../../types/alert";
import PageHeader from "../../components/common/pageHeader";

const AlertsPage: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchAlerts() {
      try {
        setLoading(true);
        const data = await getAlerts();
        setAlerts(data);
      } catch (error) {
        console.error("Failed to fetch alerts:", error);
        message.error("Failed to load alerts");
      } finally {
        setLoading(false);
      }
    }

    fetchAlerts();
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <PageHeader title="Alerts" />

      <Table
        dataSource={alerts}
        rowKey="id"
        loading={loading}
        bordered
        columns={[
          { title: "ID", dataIndex: "id", key: "id" },
          { title: "Patient ID", dataIndex: "patient_id", key: "patient_id" },
          { title: "Type", dataIndex: "type", key: "type" },
          {
            title: "Severity",
            dataIndex: "severity",
            key: "severity",
            render: (severity: string) => <Tag>{severity}</Tag>,
          },
          { title: "Message", dataIndex: "message", key: "message" },
        ]}
      />
    </div>
  );
};

export default AlertsPage;