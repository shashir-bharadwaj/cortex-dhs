import React, { useEffect, useState } from "react";
import { Table, message, Typography } from "antd";
import type { ColumnsType } from "antd/es/table";

import { getAuditLogs } from "../../api/adminApi";
import type { AuditLog } from "../../types/audit";

const { Text, Title } = Typography;

function formatJson(value?: string) {
  if (!value) return "-";

  try {
    return JSON.stringify(JSON.parse(value), null, 2);
  } catch {
    return value;
  }
}

const AuditLogViewer: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function loadLogs() {
      try {
        setLoading(true);
        const data = await getAuditLogs();
        setLogs(data);
      } catch (error) {
        console.error("Failed to load audit logs:", error);
        message.error("Failed to load audit logs");
      } finally {
        setLoading(false);
      }
    }

    loadLogs();
  }, []);

  const columns: ColumnsType<AuditLog> = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      width: 80,
    },
    {
      title: "Timestamp",
      dataIndex: "timestamp",
      key: "timestamp",
      render: (timestamp: string) => new Date(timestamp).toLocaleString(),
      width: 180,
    },
    {
      title: "User",
      dataIndex: "user_id",
      key: "user_id",
      render: (userId?: number) => userId ?? "-",
      width: 100,
    },
    {
      title: "Model",
      dataIndex: "model",
      key: "model",
      width: 140,
    },
    {
      title: "Action",
      dataIndex: "action",
      key: "action",
      width: 120,
    },
    {
      title: "Object",
      dataIndex: "object_id",
      key: "object_id",
      render: (objectId?: number) => objectId ?? "-",
      width: 100,
    },
    {
      title: "Before",
      dataIndex: "before_data",
      key: "before_data",
      render: (value?: string) => (
        <Text code style={{ whiteSpace: "pre-wrap", fontSize: 12 }}>
          {formatJson(value)}
        </Text>
      ),
      width: 320,
    },
    {
      title: "After",
      dataIndex: "after_data",
      key: "after_data",
      render: (value?: string) => (
        <Text code style={{ whiteSpace: "pre-wrap", fontSize: 12 }}>
          {formatJson(value)}
        </Text>
      ),
      width: 320,
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Title level={3}>Audit Logs</Title>

      <Table
        rowKey="id"
        columns={columns}
        dataSource={logs}
        loading={loading}
        bordered
        scroll={{ x: 1500 }}
      />
    </div>
  );
};

export default AuditLogViewer;