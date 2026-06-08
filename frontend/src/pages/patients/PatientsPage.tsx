import React, { useEffect, useState } from "react";
import { Table, message } from "antd";
import { useNavigate } from "react-router-dom";
import { getPatients } from "../../api/patientApi";
import { Patient } from "../../types/patient";
import PageHeader from "../../components/common/pageHeader";

const PatientsPage: React.FC = () => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchPatients() {
      try {
        setLoading(true);
        const data = await getPatients();
        setPatients(data);
      } catch (error) {
        console.error("Failed to fetch patients:", error);
        message.error("Failed to load patients");
      } finally {
        setLoading(false);
      }
    }

    fetchPatients();
  }, []);

  const columns = [
    { title: "ID", dataIndex: "id", key: "id" },
    {
      title: "Name",
      dataIndex: "first_name",
      key: "first_name",
      render: (_: unknown, record: Patient) =>
        `${record.first_name} ${record.last_name}`,
    },
    { title: "Bed", dataIndex: "bed_id", key: "bed_id" },
    {
      title: "Admission",
      dataIndex: "admission_time",
      key: "admission_time",
      render: (t: string) => new Date(t).toLocaleString(),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <PageHeader title="Patients" />

      <Table
        dataSource={patients}
        columns={columns}
        rowKey="id"
        bordered
        loading={loading}
        onRow={(record) => ({
          onClick: () => navigate(`/patients/${record.id}`),
          style: { cursor: "pointer" },
        })}
      />
    </div>
  );
};

export default PatientsPage;