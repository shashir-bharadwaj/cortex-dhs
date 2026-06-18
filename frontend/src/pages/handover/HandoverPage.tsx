import React, { useEffect, useState } from "react";
import { Badge, Button, Card, Col, Row, Spin, Tag, Typography, message } from "antd";
import { AlertOutlined, FileTextOutlined } from "@ant-design/icons";
import { getShiftHandoverSummary } from "../../api/handoverApi";
import { HandoverPatientCard, ShiftHandoverSummary } from "../../types/handover";
import PageHeader from "../../components/common/pageHeader";

const { Text, Title } = Typography;

const VitalBadge: React.FC<{ label: string; value?: number | string }> = ({ label, value }) => (
  <div style={{ textAlign: "center" }}>
    <div style={{ fontSize: 11, color: "#888" }}>{label}</div>
    <div style={{ fontWeight: 700, fontSize: 14 }}>{value ?? "—"}</div>
  </div>
);

const PatientHandoverCard: React.FC<{ card: HandoverPatientCard }> = ({ card }) => {
  const hasCriticalAlarms = card.unacknowledgedAlarms > 0;

  return (
    <Card
      style={{
        borderRadius: 8,
        border: hasCriticalAlarms ? "2px solid #ff4d4f" : undefined,
        position: "relative",
      }}
      bodyStyle={{ padding: 16 }}
    >
      {hasCriticalAlarms && (
        <div style={{ position: "absolute", top: 12, right: 12 }}>
          <Badge count={card.unacknowledgedAlarms} color="red" />
        </div>
      )}

      <div style={{ marginBottom: 8 }}>
        <Text type="secondary" style={{ fontSize: 12 }}>
          {card.bedLabel}
        </Text>
        <Title level={5} style={{ margin: 0 }}>
          {card.patientName}
        </Title>
        <Text type="secondary" style={{ fontSize: 12 }}>
          {[card.age && `${card.age}y`, card.gender, card.diagnosis]
            .filter(Boolean)
            .join(" · ")}
        </Text>
      </div>

      <Row gutter={8} style={{ marginBottom: 12 }}>
        <Col span={6}><VitalBadge label="HR" value={card.vitals.hr ? Math.round(card.vitals.hr) : undefined} /></Col>
        <Col span={6}><VitalBadge label="SpO2" value={card.vitals.spo2 ? `${Math.round(card.vitals.spo2)}%` : undefined} /></Col>
        <Col span={6}><VitalBadge label="BP" value={card.vitals.bp} /></Col>
        <Col span={6}><VitalBadge label="RR" value={card.vitals.rr ? Math.round(card.vitals.rr) : undefined} /></Col>
      </Row>

      {card.doctor && (
        <Text style={{ fontSize: 12 }}>
          <span style={{ color: "#888" }}>Doctor: </span>{card.doctor}
        </Text>
      )}

      <div style={{ marginTop: 8, display: "flex", gap: 8, flexWrap: "wrap" }}>
        {hasCriticalAlarms && (
          <Tag color="red" icon={<AlertOutlined />}>
            {card.unacknowledgedAlarms} unacknowledged alarm{card.unacknowledgedAlarms > 1 ? "s" : ""}
          </Tag>
        )}
        {card.pendingTasks > 0 && (
          <Tag color="orange">{card.pendingTasks} pending task{card.pendingTasks > 1 ? "s" : ""}</Tag>
        )}
        {card.ventilatorActive && <Tag color="blue">Ventilator active</Tag>}
      </div>

      {card.latestNote && (
        <div
          style={{
            marginTop: 10,
            padding: 8,
            background: "#fafafa",
            borderRadius: 4,
            fontSize: 12,
          }}
        >
          <FileTextOutlined style={{ marginRight: 4, color: "#888" }} />
          <Text style={{ fontSize: 12 }}>"{card.latestNote.text}"</Text>
          <div>
            <Text type="secondary" style={{ fontSize: 11 }}>
              — {card.latestNote.author}
            </Text>
          </div>
        </div>
      )}
    </Card>
  );
};

const HandoverPage: React.FC = () => {
  const [data, setData] = useState<ShiftHandoverSummary | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchHandover() {
      try {
        setLoading(true);
        const result = await getShiftHandoverSummary();
        setData(result);
      } catch {
        message.error("Failed to load shift handover");
      } finally {
        setLoading(false);
      }
    }
    fetchHandover();
  }, []);

  if (loading) {
    return (
      <div style={{ display: "flex", justifyContent: "center", padding: 48 }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
        <PageHeader title="Shift Handover Summary" />
        <Button type="primary">Generate Report</Button>
      </div>

      {data && (
        <Text type="secondary" style={{ display: "block", marginBottom: 24 }}>
          Current Shift: {data.shift.name} ({data.shift.start}–{data.shift.end})
        </Text>
      )}

      <Row gutter={[16, 16]}>
        {data?.patients.map((card) => (
          <Col key={card.patientId} xs={24} sm={12} lg={8}>
            <PatientHandoverCard card={card} />
          </Col>
        ))}
      </Row>

      {(data?.patients.length ?? 0) === 0 && !loading && (
        <div style={{ textAlign: "center", padding: 48, color: "#999" }}>
          No patients in current shift
        </div>
      )}
    </div>
  );
};

export default HandoverPage;
