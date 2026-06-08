import React, { useEffect, useState } from "react";
import { Table, message, Tag } from "antd";
import type { ColumnsType } from "antd/es/table";

import { getDevices } from "../../api/deviceApi";
import type { Device } from "../../types/device";
import PageHeader from "../../components/common/pageHeader";

const DevicesPage: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchDevices() {
      try {
        setLoading(true);
        const data = await getDevices();
        setDevices(data);
      } catch (error) {
        console.error("Failed to fetch devices:", error);
        message.error("Failed to load devices");
      } finally {
        setLoading(false);
      }
    }

    fetchDevices();
  }, []);

  const columns: ColumnsType<Device> = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
    },
    {
      title: "Bed",
      dataIndex: "bed_id",
      key: "bed_id",
    },
    {
      title: "Type",
      dataIndex: "device_type_name",
      key: "device_type_name",
    },
    {
      title: "Serial",
      dataIndex: "serial_number",
      key: "serial_number",
      render: (serial?: string) => serial || "-",
    },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (status: string) => {
        let color = "default";

        if (status.toLowerCase() === "active") color = "green";
        else if (status.toLowerCase() === "offline") color = "red";
        else if (status.toLowerCase() === "warning") color = "orange";

        return <Tag color={color}>{status.toUpperCase()}</Tag>;
      },
    },
    {
      title: "Last Seen",
      dataIndex: "last_seen",
      key: "last_seen",
      render: (t: string) => new Date(t).toLocaleString(),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <PageHeader title="Devices" />

      <Table
        dataSource={devices}
        columns={columns}
        rowKey="id"
        bordered
        loading={loading}
      />
    </div>
  );
};

export default DevicesPage;