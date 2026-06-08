import React, { useEffect, useState } from "react";
import { Table, message } from "antd";
import { getDevices } from "../api/deviceApi";
import { Device } from "../types/device";
import PageHeader from "../components/common/pageHeader";

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

  return (
    <div style={{ padding: 24 }}>
      <PageHeader title="Devices" />

      <Table
        dataSource={devices}
        rowKey="id"
        loading={loading}
        bordered
        columns={[
          { title: "ID", dataIndex: "id", key: "id" },
          { title: "Name", dataIndex: "name", key: "name" },
          { title: "Type", dataIndex: "type", key: "type" },
          { title: "Status", dataIndex: "status", key: "status" },
        ]}
      />
    </div>
  );
};

export default DevicesPage;