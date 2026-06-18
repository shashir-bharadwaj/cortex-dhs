import React, { useEffect, useState } from "react";
import { Card, Col, Row, Spin, Statistic, Tag, Typography, message } from "antd";
import { getActiveInfusions } from "../../api/medicationApi";
import { ActiveInfusion } from "../../types/activeInfusion";
import PageHeader from "../../components/common/pageHeader";

const { Text } = Typography;

const MedicationPage: React.FC = () => {
  const [infusions, setInfusions] = useState<ActiveInfusion[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchInfusions() {
      try {
        setLoading(true);
        const data = await getActiveInfusions();
        setInfusions(data);
      } catch {
        message.error("Failed to load active infusions");
      } finally {
        setLoading(false);
      }
    }
    fetchInfusions();
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
      <PageHeader title="Infusion & Medication" />
      <Text type="secondary" style={{ display: "block", marginBottom: 24 }}>
        {infusions.length} active infusions
      </Text>

      <Row gutter={[16, 16]}>
        {infusions.map((infusion) => (
          <Col key={infusion.id} xs={24} sm={12} lg={8}>
            <Card
              title={
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <Text strong>{infusion.drugName}</Text>
                  <Tag color="green">{infusion.status.toLowerCase()}</Tag>
                </div>
              }
              bordered
              style={{ borderRadius: 8 }}
            >
              <Text type="secondary">
                {infusion.bedLabel} · {infusion.patientName}
              </Text>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 12 }}>
                <div>
                  <Text type="secondary" style={{ fontSize: 12 }}>Dosage</Text>
                  <div><Text strong>{infusion.dose ?? "—"}</Text></div>
                </div>
                <div>
                  <Text type="secondary" style={{ fontSize: 12 }}>Rate</Text>
                  <div>
                    <Text strong>
                      {infusion.rateMlHr != null ? `${infusion.rateMlHr} ml/hr` : "—"}
                    </Text>
                  </div>
                </div>
                <div>
                  <Text type="secondary" style={{ fontSize: 12 }}>Remaining</Text>
                  <div>
                    <Text strong>
                      {infusion.remainingVolMl != null ? `${infusion.remainingVolMl} ml` : "—"}
                    </Text>
                  </div>
                </div>
                <div>
                  <Text type="secondary" style={{ fontSize: 12 }}>Est. End</Text>
                  <div>
                    <Text strong>
                      {infusion.estEndTime
                        ? new Date(infusion.estEndTime).toLocaleTimeString([], {
                            hour: "2-digit",
                            minute: "2-digit",
                          })
                        : "—"}
                    </Text>
                  </div>
                </div>
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      {infusions.length === 0 && (
        <div style={{ textAlign: "center", padding: 48, color: "#999" }}>
          No active infusions
        </div>
      )}
    </div>
  );
};

export default MedicationPage;
