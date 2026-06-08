import React, { useEffect, useState } from "react";
import { Table, message } from "antd";
import { getVitals } from "../../api/vitalsApi";
import { Vital } from "../../types/vital";
import PageHeader from "../../components/common/pageHeader";

const VitalsPage: React.FC = () => {
  const [vitals, setVitals] = useState<Vital[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchVitals() {
      try {
        setLoading(true);
        const data = await getVitals();
        setVitals(data);
      } catch (error) {
        console.error("Failed to fetch vitals:", error);
        message.error("Failed to load vitals");
      } finally {
        setLoading(false);
      }
    }

    fetchVitals();
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <PageHeader title="Vitals" />

      <Table
        dataSource={vitals}
        rowKey="id"
        loading={loading}
        bordered
        columns={[
          { title: "ID", dataIndex: "id", key: "id" },
          { title: "Patient ID", dataIndex: "patient_id", key: "patient_id" },
          { title: "Heart Rate", dataIndex: "heart_rate", key: "heart_rate" },
          { title: "SpO2", dataIndex: "spo2", key: "spo2" },
          {
            title: "Recorded At",
            dataIndex: "recorded_at",
            key: "recorded_at",
          },
        ]}
      />
    </div>
  );
};

export default VitalsPage;