import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Button,
  Card,
  Col,
  DatePicker,
  Descriptions,
  Empty,
  Row,
  Spin,
  Table,
  Tabs,
  Tag,
  Typography,
  message,
} from "antd";
import type { ColumnsType } from "antd/es/table";
import dayjs from "dayjs";

import { getPatientById, getPatientFlowsheet } from "../../api/patientApi";
import type { Patient } from "../../types/patient";
import type { Flowsheet, FlowsheetRow } from "../../types/flowsheet";

const { Title, Text } = Typography;

// ---------------------------------------------------------------------------
// Flowsheet tab
// ---------------------------------------------------------------------------

function FlowsheetTab({ patientId }: { patientId: number }) {
  const [flowsheet, setFlowsheet] = useState<Flowsheet | null>(null);
  const [loading, setLoading] = useState(false);
  const [date, setDate] = useState<dayjs.Dayjs>(dayjs());

  async function load(d: dayjs.Dayjs) {
    try {
      setLoading(true);
      const data = await getPatientFlowsheet(patientId, d.format("YYYY-MM-DD"));
      setFlowsheet(data);
    } catch (err) {
      console.error("Flowsheet load failed:", err);
      message.error("Failed to load flowsheet data");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load(date);
  }, [patientId]);

  function handleDateChange(d: dayjs.Dayjs | null) {
    if (!d) return;
    setDate(d);
    load(d);
  }

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: 48 }}>
        <Spin size="large" />
      </div>
    );
  }

  const hours = flowsheet?.hours ?? [];
  const rows = flowsheet?.rows ?? [];

  // Build Ant Design table columns: one for the parameter label, one per hour
  const columns: ColumnsType<FlowsheetRow> = [
    {
      title: "Parameter",
      dataIndex: "parameter",
      key: "parameter",
      fixed: "left",
      width: 130,
      render: (val: string) => <Text strong>{val}</Text>,
    },
    ...hours.map((h) => ({
      title: `${String(h).padStart(2, "0")}:00`,
      key: `h${h}`,
      width: 72,
      align: "center" as const,
      render: (_: unknown, row: FlowsheetRow) => {
        const val = row.values[String(h)];
        if (val === null || val === undefined) return <Text type="secondary">—</Text>;
        return <Text>{val}</Text>;
      },
    })),
  ];

  return (
    <div>
      <Row align="middle" gutter={16} style={{ marginBottom: 16 }}>
        <Col>
          <Text strong>Date:</Text>
        </Col>
        <Col>
          <DatePicker
            value={date}
            onChange={handleDateChange}
            allowClear={false}
            style={{ width: 160 }}
          />
        </Col>
        <Col>
          <Button onClick={() => load(date)}>Refresh</Button>
        </Col>
      </Row>

      {!flowsheet || hours.length === 0 ? (
        <Empty description="No hourly vitals recorded for this date" />
      ) : (
        <Table<FlowsheetRow>
          rowKey="parameter"
          dataSource={rows}
          columns={columns}
          pagination={false}
          bordered
          scroll={{ x: "max-content" }}
          size="small"
          rowClassName={(_, index) =>
            index % 2 === 0 ? "flowsheet-row-even" : "flowsheet-row-odd"
          }
        />
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Overview tab
// ---------------------------------------------------------------------------

function OverviewTab({ patient }: { patient: Patient }) {
  const genderColor: Record<string, string> = {
    male: "blue",
    female: "magenta",
    other: "purple",
  };

  return (
    <Card bordered={false}>
      <Descriptions
        bordered
        column={{ xs: 1, sm: 2, md: 3 }}
        size="small"
        labelStyle={{ fontWeight: 600, width: 140 }}
      >
        <Descriptions.Item label="Name">{patient.name}</Descriptions.Item>
        <Descriptions.Item label="MRN">{patient.mrn ?? "—"}</Descriptions.Item>
        <Descriptions.Item label="CR Number">
          {patient.crNumber ?? "—"}
        </Descriptions.Item>
        <Descriptions.Item label="Age">{patient.age ?? "—"}</Descriptions.Item>
        <Descriptions.Item label="Gender">
          {patient.gender ? (
            <Tag color={genderColor[patient.gender.toLowerCase()] ?? "default"}>
              {patient.gender.toUpperCase()}
            </Tag>
          ) : (
            "—"
          )}
        </Descriptions.Item>
        <Descriptions.Item label="Blood Group">
          {patient.bloodGroup ?? "—"}
        </Descriptions.Item>
        <Descriptions.Item label="Diagnosis" span={2}>
          {patient.diagnosis ?? "—"}
        </Descriptions.Item>
        <Descriptions.Item label="Attending Doctor">
          {patient.doctor ?? "—"}
        </Descriptions.Item>
        <Descriptions.Item label="Admission">
          {patient.admissionTime
            ? new Date(patient.admissionTime).toLocaleString()
            : "—"}
        </Descriptions.Item>
        <Descriptions.Item label="Status">
          <Tag color={patient.status === "admitted" ? "green" : "default"}>
            {patient.status?.toUpperCase()}
          </Tag>
        </Descriptions.Item>
        <Descriptions.Item label="Weight">
          {patient.weight != null ? `${patient.weight} kg` : "—"}
        </Descriptions.Item>
        <Descriptions.Item label="Height">
          {patient.height != null ? `${patient.height} cm` : "—"}
        </Descriptions.Item>
        <Descriptions.Item label="BSA">
          {patient.bsa != null ? `${patient.bsa} m²` : "—"}
        </Descriptions.Item>
        <Descriptions.Item label="Contact">
          {patient.contactNumber ?? "—"}
        </Descriptions.Item>
      </Descriptions>

      {patient.history && patient.history.length > 0 && (
        <div style={{ marginTop: 16 }}>
          <Text strong>History</Text>
          <ul style={{ marginTop: 4 }}>
            {patient.history.map((h, i) => (
              <li key={i}>{h}</li>
            ))}
          </ul>
        </div>
      )}

      {patient.comorbidities && patient.comorbidities.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <Text strong>Comorbidities</Text>
          <div style={{ marginTop: 4 }}>
            {patient.comorbidities.map((c, i) => (
              <Tag key={i} color="orange" style={{ marginBottom: 4 }}>
                {c}
              </Tag>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

const PatientDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [patient, setPatient] = useState<Patient | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");

  const patientId = id ? parseInt(id, 10) : NaN;

  useEffect(() => {
    if (!id || isNaN(patientId)) return;

    setLoading(true);
    getPatientById(patientId)
      .then(setPatient)
      .catch((err) => {
        console.error("Failed to load patient:", err);
        message.error("Failed to load patient");
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div style={{ padding: 40, textAlign: "center" }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!patient) {
    return (
      <div style={{ padding: 24 }}>
        <Button onClick={() => navigate(-1)} style={{ marginBottom: 16 }}>
          ← Back
        </Button>
        <Empty description="Patient not found" />
      </div>
    );
  }

  const tabItems = [
    {
      key: "overview",
      label: "Overview",
      children: <OverviewTab patient={patient} />,
    },
    {
      key: "flowsheet",
      label: "Flowsheet",
      children: <FlowsheetTab patientId={patientId} />,
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Button onClick={() => navigate(-1)} style={{ marginBottom: 16 }}>
        ← Back
      </Button>

      <Card style={{ marginBottom: 16 }}>
        <Row justify="space-between" align="middle">
          <Col>
            <Title level={4} style={{ margin: 0 }}>
              {patient.name}
            </Title>
            <Text type="secondary">
              {patient.diagnosis ?? ""}
              {patient.mrn ? ` · MRN: ${patient.mrn}` : ""}
            </Text>
          </Col>
          <Col>
            <Tag
              color={patient.status === "admitted" ? "green" : "default"}
              style={{ fontSize: 14, padding: "4px 12px" }}
            >
              {patient.status?.toUpperCase()}
            </Tag>
          </Col>
        </Row>
      </Card>

      <Tabs
        activeKey={activeTab}
        onChange={setActiveTab}
        items={tabItems}
        type="card"
      />
    </div>
  );
};

export default PatientDetailPage;
