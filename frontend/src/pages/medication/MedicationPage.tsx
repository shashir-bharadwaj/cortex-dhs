import React, { useEffect, useState } from "react";
import { Card, Col, Input, InputNumber, Row, Spin, Statistic, Tag, Typography, message } from "antd";
import { getActiveInfusions } from "../../api/medicationApi";
import { ActiveInfusion } from "../../types/activeInfusion";
import PageHeader from "../../components/common/pageHeader";
import { CloseOutlined, EditOutlined, SaveOutlined } from "@ant-design/icons";

const { Text } = Typography;

const MedicationPage: React.FC = () => {
  const [infusions, setInfusions] = useState<ActiveInfusion[]>([]);
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
const [editData, setEditData] = useState<any>({});

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
const handleEdit = (infusion: any) => {
  setEditingId(infusion.id);
  setEditData({ ...infusion });
};

const handleSave = () => {
  setInfusions((prev: any[]) =>
    prev.map((item) =>
      item.id === editingId ? { ...item, ...editData } : item
    )
  );
  setEditingId(null);
};

const handleCancel = () => {
  setEditingId(null);
  setEditData({});
};
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
    {infusions.map((infusion) => {
      const isEditing = editingId === infusion.id;

      return (
        <Col key={infusion.id} xs={24} sm={12} lg={8}>
          <Card
            title={
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <Text strong>
                  {isEditing ? (
                    <Input
                      value={editData.drugName}
                      onChange={(e) =>
                        setEditData({ ...editData, drugName: e.target.value })
                      }
                    />
                  ) : (
                    infusion.drugName
                  )}
                </Text>

                <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                  <Tag color="green">{infusion.status.toLowerCase()}</Tag>

                  {!isEditing ? (
                    <EditOutlined
                      style={{ cursor: "pointer" }}
                      onClick={() => handleEdit(infusion)}
                    />
                  ) : (
                    <>
                      <SaveOutlined
                        style={{ cursor: "pointer", color: "green" }}
                        onClick={handleSave}
                      />

                      <CloseOutlined
                        style={{ cursor: "pointer", color: "red" }}
                        onClick={handleCancel}
                      />
                    </>
                  )}
                </div>
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
                <Text type="secondary" style={{ fontSize: 12 }}>
                  Dosage
                </Text>

                <div>
                  {isEditing ? (
                    <Input
                      value={editData.dose}
                      onChange={(e) =>
                        setEditData({ ...editData, dose: e.target.value })
                      }
                    />
                  ) : (
                    <Text strong>{infusion.dose ?? "—"}</Text>
                  )}
                </div>
              </div>


              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>
                  Rate
                </Text>

                <div>
                  {isEditing ? (
                    <InputNumber
                      value={editData.rateMlHr}
                      onChange={(value) =>
                        setEditData({ ...editData, rateMlHr: value })
                      }
                    />
                  ) : (
                    <Text strong>
                      {infusion.rateMlHr != null
                        ? `${infusion.rateMlHr} ml/hr`
                        : "—"}
                    </Text>
                  )}
                </div>
              </div>


              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>
                  Remaining
                </Text>

                <div>
                  {isEditing ? (
                    <InputNumber
                      value={editData.remainingVolMl}
                      onChange={(value) =>
                        setEditData({
                          ...editData,
                          remainingVolMl: value,
                        })
                      }
                    />
                  ) : (
                    <Text strong>
                      {infusion.remainingVolMl != null
                        ? `${infusion.remainingVolMl} ml`
                        : "—"}
                    </Text>
                  )}
                </div>
              </div>


              <div>
                <Text type="secondary" style={{ fontSize: 12 }}>
                  Est. End
                </Text>

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
      );
    })}
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
