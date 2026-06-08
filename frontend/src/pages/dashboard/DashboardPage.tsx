import React, { useEffect, useState } from "react";
import { Table, message, Tag } from "antd";
import { useAuth } from "../../auth/AuthContext";
import { getBedOverview } from "../../api/dashboardApi";
import { BedOverview } from "../../types/dashboard";
import PageHeader from "../../components/common/pageHeader";

const DashboardPage: React.FC = () => {
  const { logout } = useAuth();
  const [beds, setBeds] = useState<BedOverview[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchBeds() {
      try {
        setLoading(true);
        const data = await getBedOverview();
        setBeds(data);
      } catch (error) {
        console.error("Failed to fetch bed overview:", error);
        message.error("Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    }

    fetchBeds();
  }, []);

  const columns = [
    {
      title: "Bed",
      dataIndex: "bed_number",
      key: "bed_number",
    },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (status: BedOverview["status"]) => (
        <Tag color={status === "occupied" ? "red" : "green"}>
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: "Patient",
      dataIndex: "patient",
      key: "patient",
      render: (patient: BedOverview["patient"]) =>
        patient ? `${patient.first_name} ${patient.last_name}` : "-",
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <PageHeader
        title="Bed Overview"
        actionLabel="Logout"
        onActionClick={logout}
      />

      <Table
        dataSource={beds}
        columns={columns}
        rowKey="id"
        pagination={false}
        bordered
        loading={loading}
      />
    </div>
  );
};

export default DashboardPage;