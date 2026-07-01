import React, { useEffect, useState } from "react";
import { message, Tag, Typography } from "antd";
import { Pencil, Trash2 } from "lucide-react";
import { getAuditLogs } from "../../api/adminApi";
import CommonTable from "../shared/commontable";



type AuditLogRow = {
  id: number;
  time: string;
  user: string;
  role: string;
  action: string;
  module: string;
  ip: string;
};

const { Title, Text } = Typography;


const getRoleTag = (role: string) => {
  const colors: any = {
    Admin: "green",
    Doctor: "blue",
    Nurse: "purple",
    Technician: "cyan",
    "Hospital IT": "geekblue",
  };

  return <Tag color={colors[role] || "default"}>{role}</Tag>;
};

/* ================= COMPONENT ================= */

const AuditLogsPage = () => {
  const [logs, setLogs] = useState<AuditLogRow[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadLogs = async () => {
      setLoading(true);

      try {
        const response = await getAuditLogs();
        setLogs(response);
      } catch (error) {
        console.error("Failed to load audit logs:", error);
        message.error("Failed to load audit logs");
      } finally {
        setLoading(false);
      }
    };

    loadLogs();
  }, []);

  const columns = [
    {
      title: "Timestamp",
      dataIndex: "time",
    },
    {
      title: "User",
      dataIndex: "user",
      render: (text: string) => <b>{text}</b>,
    },
    {
      title: "Role",
      dataIndex: "role",
      render: (role: string) => getRoleTag(role),
    },
    {
      title: "Action",
      dataIndex: "action",
    },
    {
      title: "Module",
      dataIndex: "module",
    },
    {
      title: "IP Address",
      dataIndex: "ip",
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      {/* Header */}
      <div style={{ marginBottom: 16 }}>
        <Title level={3}>Audit Logs</Title>
        <Text type="secondary">
          Track system activity and user actions
        </Text>
      </div>

      {/* Table */}
      <CommonTable
        columns={columns}
        data={logs}
        renderActions={(row) => (
          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <Pencil
              size={18}
              onClick={() => console.log("Edit", row)}
              style={{ cursor: "pointer", color: "#2563EB" }}
            />

            <Trash2
              size={18}
              onClick={() => console.log("Delete", row)}
              style={{ cursor: "pointer", color: "#dc2626" }}
            />
          </div>
        )}
      />
    </div>

  );
};

export default AuditLogsPage;