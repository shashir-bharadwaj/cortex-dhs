import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Card,
  Typography,
  Table,
  Button,
  Modal,
  Form,
  Input,
  DatePicker,
  Tag,
  message,
  Row,
  Col,
  Spin,
} from "antd";
import type { ColumnsType } from "antd/es/table";

import {
  getPatientById,
  getPatientLines,
  getPatientAiSuggestions,
  createPatientLine,
  markLineRemoved,
} from "../../api/patientApi";

import type { Patient } from "../../types/patient";
import type { Line } from "../../types/line";
import type { AISuggestion } from "../../types/ai";

const { Title, Paragraph } = Typography;

const PatientDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [patient, setPatient] = useState<Patient | null>(null);
  const [lines, setLines] = useState<Line[]>([]);
  const [aiSuggestion, setAiSuggestion] = useState<AISuggestion | null>(null);

  const [loadingPatient, setLoadingPatient] = useState(false);
  const [loadingLines, setLoadingLines] = useState(false);
  const [submittingLine, setSubmittingLine] = useState(false);

  const [lineModalVisible, setLineModalVisible] = useState(false);
  const [form] = Form.useForm();

  const patientId = id ?? "";

  async function fetchPatient() {
    try {
      setLoadingPatient(true);
      const data = await getPatientById(patientId);
      setPatient(data);
    } catch (error) {
      console.error("Failed to load patient:", error);
      message.error("Failed to load patient");
    } finally {
      setLoadingPatient(false);
    }
  }

  async function fetchLines() {
    try {
      setLoadingLines(true);
      const data = await getPatientLines(patientId);
      setLines(data);
    } catch (error) {
      console.error("Failed to load lines:", error);
      message.error("Failed to load lines");
    } finally {
      setLoadingLines(false);
    }
  }

  async function fetchAiSuggestion() {
    try {
      const data = await getPatientAiSuggestions(patientId);
      setAiSuggestion(data);
    } catch (error) {
      // AI suggestion is optional
      console.warn("AI suggestions unavailable:", error);
    }
  }

  useEffect(() => {
    if (!patientId) return;

    fetchPatient();
    fetchLines();
    fetchAiSuggestion();
  }, [patientId]);

  async function handleAddLine() {
    try {
      const values = await form.validateFields();

      setSubmittingLine(true);

      await createPatientLine(patientId, {
        type: values.type,
        insertion_time: values.insertion_time?.toISOString(),
        expected_removal_time: values.expected_removal_time?.toISOString(),
        notes: values.notes,
      });

      message.success("Line added");
      setLineModalVisible(false);
      form.resetFields();
      fetchLines();
    } catch (error) {
      // validation errors handled by form
      if (error) {
        console.error("Failed to add line:", error);
      }
    } finally {
      setSubmittingLine(false);
    }
  }

  async function handleMarkRemoved(record: Line) {
    try {
      await markLineRemoved(record.id);
      message.success("Line marked as removed");
      fetchLines();
    } catch (error) {
      console.error("Failed to update line:", error);
      message.error("Failed to update line");
    }
  }

  const columns: ColumnsType<Line> = [
    {
      title: "Type",
      dataIndex: "type",
      key: "type",
    },
    {
      title: "Inserted",
      dataIndex: "insertion_time",
      key: "insertion_time",
      render: (t: string) => new Date(t).toLocaleString(),
    },
    {
      title: "Due",
      dataIndex: "expected_removal_time",
      key: "expected_removal_time",
      render: (t?: string | null) =>
        t ? new Date(t).toLocaleString() : "-",
    },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (status: string, record: Line) => {
        let color = "green";

        if (status === "removed") color = "volcano";

        if (record.expected_removal_time && !record.removed_time) {
          const due = new Date(record.expected_removal_time);
          if (due < new Date()) color = "orange";
        }

        return <Tag color={color}>{status.toUpperCase()}</Tag>;
      },
    },
    {
      title: "Notes",
      dataIndex: "notes",
      key: "notes",
      render: (notes?: string) => notes || "-",
    },
    {
      title: "Action",
      key: "action",
      render: (_: unknown, record: Line) =>
        record.removed_time ? null : (
          <Button size="small" onClick={() => handleMarkRemoved(record)}>
            Mark Removed
          </Button>
        ),
    },
  ];

  if (loadingPatient && !patient) {
    return (
      <div style={{ padding: 24 }}>
        <Spin />
      </div>
    );
  }

  if (!patient) {
    return (
      <div style={{ padding: 24 }}>
        <Button onClick={() => navigate(-1)} style={{ marginBottom: 16 }}>
          Back
        </Button>
        <Paragraph>Patient not found.</Paragraph>
      </div>
    );
  }

  return (
    <div style={{ padding: 24 }}>
      <Button onClick={() => navigate(-1)} style={{ marginBottom: 16 }}>
        Back
      </Button>

      <Card style={{ marginBottom: 24 }}>
        <Title level={4}>
          {patient.first_name} {patient.last_name}
        </Title>

        <Paragraph>
          <strong>Bed:</strong> {patient.bed_id}
        </Paragraph>

        <Paragraph>
          <strong>Admission:</strong>{" "}
          {new Date(patient.admission_time).toLocaleString()}
        </Paragraph>

        {patient.date_of_birth && (
          <Paragraph>
            <strong>DOB:</strong>{" "}
            {new Date(patient.date_of_birth).toLocaleDateString()}
          </Paragraph>
        )}

        {patient.gender && (
          <Paragraph>
            <strong>Gender:</strong> {patient.gender}
          </Paragraph>
        )}

        {aiSuggestion && (
          <div style={{ marginTop: 16 }}>
            <Title level={5}>AI Suggestions</Title>

            <Paragraph>
              <strong>Risk Score:</strong>{" "}
              {(aiSuggestion.risk_score * 100).toFixed(1)}%
            </Paragraph>

            <ul>
              {aiSuggestion.recommendations.map((rec, idx) => (
                <li key={idx}>{rec}</li>
              ))}
            </ul>

            <Paragraph>
              <i>{aiSuggestion.summary}</i>
            </Paragraph>
          </div>
        )}
      </Card>

      <Row justify="space-between" align="middle" style={{ marginBottom: 16 }}>
        <Col>
          <Title level={5}>Lines & Tubes</Title>
        </Col>
        <Col>
          <Button type="primary" onClick={() => setLineModalVisible(true)}>
            Add Line/Tube
          </Button>
        </Col>
      </Row>

      <Table
        rowKey="id"
        columns={columns}
        dataSource={lines}
        loading={loadingLines}
        pagination={false}
        bordered
      />

      <Modal
        title="Add Line or Tube"
        open={lineModalVisible}
        onOk={handleAddLine}
        onCancel={() => setLineModalVisible(false)}
        confirmLoading={submittingLine}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="type"
            label="Type"
            rules={[{ required: true, message: "Please enter the type" }]}
          >
            <Input placeholder="e.g., Central Line" />
          </Form.Item>

          <Form.Item
            name="insertion_time"
            label="Insertion Time"
            rules={[
              { required: true, message: "Please select insertion time" },
            ]}
          >
            <DatePicker showTime style={{ width: "100%" }} />
          </Form.Item>

          <Form.Item
            name="expected_removal_time"
            label="Expected Removal Time"
          >
            <DatePicker showTime style={{ width: "100%" }} />
          </Form.Item>

          <Form.Item name="notes" label="Notes">
            <Input.TextArea rows={3} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default PatientDetailPage;