import React, { useEffect, useRef, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Button,
  Card,
  Col,
  DatePicker,
  Empty,
  Input,
  Modal,
  Progress,
  Row,
  Select,
  Spin,
  Table,
  Tabs,
  Tag,
  Timeline,
  Typography,
  message,
} from "antd";
import type { ColumnsType } from "antd/es/table";
import {
  HeartOutlined,
  DashboardOutlined,
  ExperimentOutlined,
  FireOutlined,
  ThunderboltOutlined,
  DownloadOutlined,
  FileTextOutlined,
  PrinterOutlined,
  CloseOutlined,
  SaveOutlined,
  EditOutlined,
} from "@ant-design/icons";
import dayjs from "dayjs";

import {
  getPatientDetails,
  getPatientFlowsheet,
  downloadVitalsCsv,
  getDailySummaryReport,
  getDischargeSummaryReport,
} from "../../api/patientApi";
import { createPatientNote, createPatientTimeline } from "../../api/notesApi";
import { useLiveVitals } from "../../hooks/useLiveVitals";
import type { LatestVital } from "../../types/patient";
import type { Flowsheet, FlowsheetRow } from "../../types/flowsheet";
import type {
  PatientDetails,
  Vital,
  VentilatorParams,
  LabData,
  FluidBalance,
  MedicationOrder,
  DeviceMaster,
  TimelineEvent,
  ClinicalNote,
  StaffAssignment,
} from "../../types/patientDetails";
import type { Patient } from "../../types/patient";
import "./PatientDetailPage.css";
import PatientModal from "./PatientModal";
import { Info } from "lucide-react";
import axios from "axios";

const { Title, Text } = Typography;

const BRAND_PURPLE = "#5b2be0";

function fmt(v: number | string | null | undefined, suffix = ""): string {
  if (v === null || v === undefined || v === "") return "—";
  return `${v}${suffix}`;
}

// ---------------------------------------------------------------------------
// Reusable building blocks
// ---------------------------------------------------------------------------

const VitalCard: React.FC<{
  icon: React.ReactNode;
  label: string;
  value: React.ReactNode;
  unit: string;
  accent: string;
}> = ({ icon, label, value, unit, accent }) => (
  <Card size="small" styles={{ body: { padding: 16 } }} style={{ height: "100%" }}>
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 6,
        color: accent,
        fontSize: 12,
        fontWeight: 600,
        letterSpacing: 0.4,
      }}
    >
      {icon}
      <span style={{ color: "#8a8a9e", textTransform: "uppercase" }}>
        {label}
      </span>
    </div>
    <div style={{ fontSize: 19, fontWeight: 700, color: "#1a1a2e", marginTop: 8 }}>
      {value}
    </div>
    <div style={{ fontSize: 12, color: "#9a9aae" }}>{unit}</div>
  </Card>
);

const LabeledRow: React.FC<{ label: string; value: React.ReactNode }> = ({
  label,
  value,
}) => (
  <div
    style={{
      display: "flex",
      justifyContent: "space-between",
      padding: "8px 0",
      borderBottom: "1px solid #f2f2f5",
      fontSize: 13,
    }}
  >
    <span style={{ color: "#8a8a9e", fontSize: 12 }}>{label}</span>
    <span style={{ color: "#1a1a2e", fontWeight: 600 }}>{value}</span>
  </div>
);

const SectionCard: React.FC<{
  title: string;
  children: React.ReactNode;
  extra?: React.ReactNode;
}> = ({ title, children, extra }) => (
  <Card
    size="small"
    style={{ marginBottom: 16 }}
    styles={{ body: { padding: "12px 16px" } }}
  >
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 6,
      }}
    >
      <Text strong style={{ fontSize: 13 }}>
        {title}
      </Text>
      {extra}
    </div>
    {children}
  </Card>
);

// ---------------------------------------------------------------------------
// Live Trends — dependency-free SVG multi-line chart
// ---------------------------------------------------------------------------

const TREND_SERIES: { key: keyof Vital; label: string; color: string }[] = [
  { key: "hr", label: "HR", color: "#2f54eb" },
  { key: "spo2", label: "SpO2", color: "#13c2c2" },
  { key: "rr", label: "RR", color: "#722ed1" },
];

function TrendChart({ vitals }: { vitals: Vital[] }) {
  const sorted = [...vitals]
    .filter((v) => v.recordedAt)
    .sort(
      (a, b) =>
        new Date(a.recordedAt!).getTime() - new Date(b.recordedAt!).getTime()
    );

  // Each vitals row typically carries a single metric, so build each series
  // independently from its own non-null samples (last N points).
  const SAMPLES = 30;
  const seriesData = TREND_SERIES.map((s) => ({
    ...s,
    points: sorted
      .filter((d) => typeof d[s.key] === "number")
      .map((d) => ({ t: d.recordedAt!, v: d[s.key] as number }))
      .slice(-SAMPLES),
  }));

  const maxLen = Math.max(0, ...seriesData.map((s) => s.points.length));
  const allVals = seriesData.flatMap((s) => s.points.map((p) => p.v));

  if (maxLen < 2 || allVals.length === 0) {
    return <Empty description="Not enough data for trends yet" />;
  }

  const W = 640;
  const H = 280;
  const padL = 34;
  const padR = 12;
  const padT = 14;
  const padB = 28;
  const maxV = Math.max(120, ...allVals);

  // Each series maps its own samples evenly across the width.
  const x = (i: number, len: number) =>
    padL + (len <= 1 ? 0 : (i / (len - 1)) * (W - padL - padR));
  const y = (val: number) => H - padB - (val / maxV) * (H - padT - padB);

  const yTicks = [0, 30, 60, 90, 120].filter((t) => t <= maxV);

  // Use the longest series for x-axis time labels.
  const axisSeries =
    seriesData.find((s) => s.points.length === maxLen) ?? seriesData[0];

  return (
    <div style={{ width: "100%", overflowX: "auto" }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" style={{ maxWidth: W }}>
        {/* gridlines + y labels */}
        {yTicks.map((t) => (
          <g key={t}>
            <line
              x1={padL}
              x2={W - padR}
              y1={y(t)}
              y2={y(t)}
              stroke="#eee"
              strokeDasharray="3 3"
            />
            <text x={4} y={y(t) + 4} fontSize={10} fill="#aaa">
              {t}
            </text>
          </g>
        ))}
        {/* x labels (first, middle, last) */}
        {[0, Math.floor((maxLen - 1) / 2), maxLen - 1].map((i) => {
          const pt = axisSeries.points[i];
          return (
            <text
              key={i}
              x={x(i, maxLen)}
              y={H - 8}
              fontSize={10}
              fill="#aaa"
              textAnchor="middle"
            >
              {pt ? dayjs(pt.t).format("HH:mm") : ""}
            </text>
          );
        })}
        {/* series lines + dots */}
        {seriesData.map((s) => {
          const len = s.points.length;
          const pts = s.points
            .map((p, i) => `${x(i, len)},${y(p.v)}`)
            .join(" ");
          return (
            <g key={s.key}>
              <polyline
                points={pts}
                fill="none"
                stroke={s.color}
                strokeWidth={2}
              />
              {s.points.map((p, i) => (
                <circle
                  key={i}
                  cx={x(i, len)}
                  cy={y(p.v)}
                  r={2.5}
                  fill="#fff"
                  stroke={s.color}
                  strokeWidth={1.5}
                />
              ))}
            </g>
          );
        })}
      </svg>
      <div style={{ display: "flex", gap: 18, justifyContent: "center", marginTop: 4 }}>
        {TREND_SERIES.map((s) => (
          <span key={s.key} style={{ display: "flex", alignItems: "center", gap: 5, fontSize: 12 }}>
            <span style={{ width: 14, height: 3, background: s.color, borderRadius: 2 }} />
            {s.label}
          </span>
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Overview tab
// ---------------------------------------------------------------------------

function OverviewTab({
  patient,
  vitals,
  latestVitals,
  ventilator,
  lab,
  fluid,
  unitId,
  lastUpdate,
}: {
  patient: Patient;
  vitals: Vital[];
  latestVitals: PatientDetails["overview"]["latestVitals"];
  ventilator?: VentilatorParams | null;
  lab?: LabData | null;
  fluid?: FluidBalance | null;
  unitId?: number | null;
  lastUpdate?: string | null;
}) {
  const lv = latestVitals;
  const nibp =
    lv?.bpSys != null && lv?.bpDia != null ? `${lv.bpSys}/${lv.bpDia}` : "—";

  return (
    <Row gutter={16}>
      {/* Left column: vitals + trends */}
      <Col xs={24} lg={16}>
        <Row gutter={[12, 12]}>
          <Col xs={12} sm={8} md={6}>
            <VitalCard
              icon={<HeartOutlined />}
              accent="#eb2f96"
              label="HR"
              value={fmt(lv?.hr)}
              unit="bpm"
            />
          </Col>
          <Col xs={12} sm={8} md={6}>
            <VitalCard
              icon={<DashboardOutlined />}
              accent="#13c2c2"
              label="SpO2"
              value={fmt(lv?.spo2)}
              unit="%"
            />
          </Col>
          <Col xs={12} sm={8} md={6}>
            <VitalCard
              icon={<ExperimentOutlined />}
              accent="#2f54eb"
              label="NIBP"
              value={nibp}
              unit="mmHg"
            />
          </Col>
          <Col xs={12} sm={8} md={6}>
            <VitalCard
              icon={<FireOutlined />}
              accent="#fa8c16"
              label="Temp"
              value={fmt(lv?.temp)}
              unit="°F"
            />
          </Col>
          <Col xs={24}>
            <VitalCard
              icon={<ThunderboltOutlined />}
              accent={BRAND_PURPLE}
              label="Respiratory Rate"
              value={fmt(lv?.rr)}
              unit="breaths/min"
            />
          </Col>
        </Row>

        <Card
          size="small"
          title={
            <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
              Live Trends
              {lastUpdate && (
                <span
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: 5,
                    fontSize: 11,
                    fontWeight: 500,
                    color: "#52c41a",
                  }}
                >
                  <span className="live-dot" />
                  Live · {dayjs(lastUpdate).format("HH:mm:ss")}
                </span>
              )}
            </span>
          }
          style={{ marginTop: 16 }}
          styles={{ body: { padding: 16 } }}
        >
          <TrendChart vitals={vitals} />
        </Card>
      </Col>

      {/* Right column: demographics + ventilator + lab + fluid */}
      <Col xs={24} lg={8}>
        <SectionCard title="Demographics">
          <LabeledRow label="Diagnosis" value={fmt(patient.diagnosis)} />
          <LabeledRow
            label="Comorbidities"
            value={
              patient.comorbidities && patient.comorbidities.length > 0
                ? patient.comorbidities.join(", ")
                : "—"
            }
          />
          <LabeledRow label="Weight" value={fmt(patient.weight, " kg")} />
          <LabeledRow label="Height" value={fmt(patient.height, " cm")} />
          <LabeledRow label="BSA" value={fmt(patient.bsa, " m²")} />
          <LabeledRow
            label="ICU Unit"
            value={unitId != null ? `Unit ${unitId}` : "—"}
          />
        </SectionCard>

        <SectionCard title="Ventilator Parameters">
          <LabeledRow label="Mode" value={fmt(ventilator?.mode)} />
          <LabeledRow
            label="FiO2"
            value={
              ventilator?.fio2 != null
                ? `${Math.round(ventilator.fio2 * 100)}%`
                : "—"
            }
          />
          <LabeledRow label="PEEP" value={fmt(ventilator?.peep, " cmH₂O")} />
          <LabeledRow label="Set RR" value={fmt(ventilator?.setRr)} />
          <LabeledRow
            label="Tidal Volume"
            value={fmt(ventilator?.tidalVolume, " mL")}
          />
        </SectionCard>

        <SectionCard title="Lab Data">
          <LabeledRow label="pH" value={fmt(lab?.ph)} />
          <LabeledRow label="PaO₂" value={fmt(lab?.pao2, " mmHg")} />
          <LabeledRow label="PaCO₂" value={fmt(lab?.paco2, " mmHg")} />
          <LabeledRow label="HCO₃" value={fmt(lab?.hco3, " mEq/L")} />
          <LabeledRow label="RBS" value={fmt(lab?.rbs, " mg/dL")} />
        </SectionCard>

        <SectionCard title="Fluid Balance (Today)">
          <LabeledRow label="Intake" value={fmt(fluid?.inMl, " mL")} />
          <LabeledRow label="Output" value={fmt(fluid?.outMl, " mL")} />
          <LabeledRow
            label="Balance"
            value={
              fluid ? (
                <span
                  style={{ color: fluid.balanceMl >= 0 ? "#52c41a" : "#ff4d4f" }}
                >
                  {fluid.balanceMl >= 0 ? "+" : ""}
                  {fluid.balanceMl} mL
                </span>
              ) : (
                "—"
              )
            }
          />
        </SectionCard>
      </Col>
    </Row>
  );
}

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

  const hours = flowsheet?.hours ?? [];
  const rows = flowsheet?.rows ?? [];

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
        if (val === null || val === undefined)
          return <Text type="secondary">—</Text>;
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

      {loading ? (
        <div style={{ textAlign: "center", padding: 48 }}>
          <Spin size="large" />
        </div>
      ) : !flowsheet || hours.length === 0 ? (
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
        />
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Devices tab
// ---------------------------------------------------------------------------

function DevicesTab({ devices }: { devices: DeviceMaster[] }) {
  if (!devices.length) return <Empty description="No devices on this bed" />;
  const columns: ColumnsType<DeviceMaster> = [
    { title: "Type", dataIndex: "device_type", key: "device_type" },
    { title: "Manufacturer", dataIndex: "manufacturer", key: "manufacturer" },
    { title: "Model", dataIndex: "model", key: "model" },
    { title: "Serial", dataIndex: "serial", key: "serial" },
    { title: "IP Address", dataIndex: "ip_address", key: "ip_address" },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (s: string) => (
        <Tag color={s?.toUpperCase() === "ACTIVE" ? "green" : "default"}>
          {s}
        </Tag>
      ),
    },
  ];
  return (
    <Table<DeviceMaster>
      rowKey="id"
      dataSource={devices}
      columns={columns}
      pagination={false}
      size="small"
    />
  );
}

// ---------------------------------------------------------------------------
// Medication tab
// ---------------------------------------------------------------------------

const STATUS_COLOR: Record<string, string> = {
  Running: "#d48806",
  Pending: "#1677ff",
  Given: "#008f3a",
  Completed: "#555",
  Cancelled: "#cf1322",
};

function MedicationTab({ medications }: { medications: MedicationOrder[] }) {
  const [medicationList, setMedicationList] = useState<MedicationOrder[]>([]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editData, setEditData] = useState<any>({});

  useEffect(() => {
    setMedicationList(medications);
  }, [medications]);

  const infusions = medicationList.filter(
    (m) => m.orderType === "Infusion" && m.status === "Running"
  );

  const startEdit = (inf: MedicationOrder) => {
    setEditingId(inf.id);
    setEditData({
      rateMlHr: inf.rateMlHr,
      remainingVolMl: inf.remainingVolMl,
      estEndTime: inf.estEndTime,
    });
  };

  const saveInfusion = () => {
    setMedicationList((prev) =>
      prev.map((item) => {
        if (item.id !== editingId) return item;

        const remaining = Number(editData.remainingVolMl);
        const end = Number(editData.estEndTime);

        return {
          ...item,
          rateMlHr: Number(editData.rateMlHr),
          remainingVolMl: remaining,
          estEndTime: editData.estEndTime,
          status: remaining === 0 && end === 0 ? "Given" : item.status,
        };
      })
    );

    setEditingId(null);
  };

  const columns: ColumnsType<MedicationOrder> = [
    {
      title: "DRUG NAME",
      dataIndex: "drugName",
      render: (v) => <Text strong>{v}</Text>,
    },
    {
      title: "TYPE",
      dataIndex: "orderType",
      render: (t) => (
        <Tag style={{ background: "#eef2f5", border: "none", fontSize: 12 }}>
          {t}
        </Tag>
      ),
    },
    {
      title: "DOSE / ROUTE",
      render: (_, r) => (
        <span>
          {fmt(r.dose)} / {fmt(r.route)}
        </span>
      ),
    },
    {
      title: "SCHEDULE",
      dataIndex: "schedule",
      render: (v) => fmt(v),
    },
    {
      title: "STATUS",
      dataIndex: "status",
      render: (s) => (
        <span
          style={{
            color: STATUS_COLOR[s],
            fontWeight: 600,
            fontSize: 13,
          }}
        >
          {s}
        </span>
      ),
    },
  ];

  return (
    <div>
      <Card
        title="Medication Orders"
        bordered={false}
        style={{
          borderRadius: 14,
          marginBottom: 24,
          overflow: "hidden",
        }}
        bodyStyle={{ padding: 0 }}
      >
        <Table
          rowKey="id"
          dataSource={medicationList}
          columns={columns}
          pagination={false}
          size="middle"
          className="medication-table"
        />
      </Card>

      {infusions.length > 0 && (
        <Card
          title="Active Infusions"
          bordered={false}
          style={{ width: 730, borderRadius: 14 }}
        >
          <Row gutter={[24, 16]}>
            {infusions.map((inf) => (
              <Col xs={24} sm={12} key={inf.id}>
                <Card style={{ borderRadius: 14 }}>
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                    }}
                  >
                    <Text strong style={{ fontSize: 16 }}>
                      {inf.drugName}
                    </Text>

                    <div>
                      <Tag
                        style={{
                          background: "#fff3bf",
                          color: "#ad6800",
                          border: "none",
                          borderRadius: 20,
                          fontSize: 12,
                        }}
                      >
                        ● Running
                      </Tag>

                      {editingId !== inf.id && (
                        <Button
                          type="text"
                          icon={<EditOutlined />}
                          onClick={() => startEdit(inf)}
                        />
                      )}
                    </div>
                  </div>

                  <div style={{ marginTop: 18, fontSize: 14 }}>
                    <InfusionRow
                      label="Rate"
                      editing={editingId === inf.id}
                      value={editData.rateMlHr}
                      display={`${inf.rateMlHr} ml/hr`}
                      onChange={(v: any) =>
                        setEditData({ ...editData, rateMlHr: v })
                      }
                    />

                    <InfusionRow
                      label="Remaining Vol"
                      editing={editingId === inf.id}
                      value={editData.remainingVolMl}
                      display={`${inf.remainingVolMl} ml`}
                      onChange={(v: any) =>
                        setEditData({
                          ...editData,
                          remainingVolMl: v,
                        })
                      }
                    />

                    <InfusionRow
                      label="Est. End Time"
                      editing={editingId === inf.id}
                      value={
                        editData.estEndTime
                          ? dayjs(editData.estEndTime).format("HH:mm")
                          : ""
                      }
                      display={
                        inf.estEndTime
                          ? dayjs(inf.estEndTime).format("HH:mm")
                          : "—"
                      }
                      onChange={(v: any) =>
                        setEditData({
                          ...editData,
                          estEndTime: v,
                        })
                      }
                    />
                  </div>

                  <Progress
                    percent={inf.remainingVolMl === 0 ? 100 : 60}
                    showInfo={false}
                  />

                  {editingId === inf.id && (
                    <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
                      <Button
                        size="small"
                        icon={<SaveOutlined />}
                        onClick={saveInfusion}
                      >
                        Save
                      </Button>

                      <Button
                        size="small"
                        icon={<CloseOutlined />}
                        onClick={() => setEditingId(null)}
                      >
                        Cancel
                      </Button>
                    </div>
                  )}
                </Card>
              </Col>
            ))}
          </Row>
        </Card>
      )}
    </div>
  );
}

function InfusionRow({
  label,
  editing,
  value,
  display,
  onChange,
}: any) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        marginBottom: 10,
      }}
    >
      <span>{label}</span>

      {editing ? (
        <Input
          size="small"
          style={{ width: 90 }}
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
      ) : (
        <Text strong>{display}</Text>
      )}
    </div>
  );
}
// ---------------------------------------------------------------------------
// Notes tab
// ---------------------------------------------------------------------------

const NOTE_TYPES = ["progress", "nursing", "order", "handover"];

function NotesTab({
  patientId,
  notes,
  onChanged,
}: {
  patientId: number;
  notes: ClinicalNote[];
  onChanged: () => void;
}) {
  const [noteType, setNoteType] = useState("progress");
  const [text, setText] = useState("");
  const [saving, setSaving] = useState(false);

  async function submit() {
    if (!text.trim()) {
      message.warning("Note text is required");
      return;
    }
    try {
      setSaving(true);
      await createPatientNote(patientId, { noteType, noteText: text });
      setText("");
      message.success("Note added");
      onChanged();
    } catch (err) {
      console.error("Add note failed:", err);
      message.error("Failed to add note");
    } finally {
      setSaving(false);
    }
  }

  const sorted = [...notes].sort(
    (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  );

  return (
    <div>
      <Card size="small" style={{ marginBottom: 16 }}>
        <Row gutter={8} align="top">
          <Col>
            <Select
              value={noteType}
              onChange={setNoteType}
              style={{ width: 140 }}
              options={NOTE_TYPES.map((t) => ({
                value: t,
                label: t.charAt(0).toUpperCase() + t.slice(1),
              }))}
            />
          </Col>
          <Col flex="auto">
            <Input.TextArea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Write a clinical note…"
              autoSize={{ minRows: 1, maxRows: 4 }}
            />
          </Col>
          <Col>
            <Button type="primary" loading={saving} onClick={submit}>
              Add
            </Button>
          </Col>
        </Row>
      </Card>

      {sorted.length === 0 ? (
        <Empty description="No clinical notes" />
      ) : (
        sorted.map((note) => (
          <Card key={note.id} size="small" style={{ marginBottom: 10 }}>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                marginBottom: 4,
              }}
            >
              <span>
                <Tag color="purple">{note.noteType}</Tag>
                <Text strong>{note.authorName}</Text>
              </span>
              <Text type="secondary" style={{ fontSize: 12 }}>
                {dayjs(note.createdAt).format("DD MMM YYYY, HH:mm")}
              </Text>
            </div>
            <Text>{note.noteText}</Text>
          </Card>
        ))
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Timeline tab
// ---------------------------------------------------------------------------

const TIMELINE_COLOR: Record<string, string> = {
  alarm: "#cf1322",
  medication: "#1677ff",
  vital: "#52c41a",
  note: "#0057a8",
  admission: "#555",
};

function TimelineTab({ events, patientId }: { events: TimelineEvent[]; patientId: number }) {
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>([]);
  const [event, setEvent] = useState("");
  const [type, setType] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setTimelineEvents(events);
  }, [events]);

  const addTimeline = async () => {
    if (!event.trim() || !type.trim()) return;

    try {
      setSaving(true);

      const response = await createPatientTimeline(patientId, {
        event,
        type,
      }); 

      setTimelineEvents((prev) => [response, ...prev]);
      setEvent("");
      setType("");
    } catch (err) {
      console.error("Add timeline event failed:", err);
      message.error("Failed to add timeline event");
    } finally {
      setSaving(false);
    }
  };

  const sorted = [...timelineEvents].sort(
    (a, b) =>
      new Date(b.time ?? 0).getTime() -
      new Date(a.time ?? 0).getTime()
  );

  return (
    <div>
      <div style={{ display: "flex", gap: 6, marginBottom: 10 }}>
        <Input
          value={event}
          placeholder="Event"
          onChange={(e) => setEvent(e.target.value)}
          style={{ height: 28, fontSize: 12 }}
        />

        <Input
          value={type}
          placeholder="Type"
          onChange={(e) => setType(e.target.value)}
          style={{ width: 120, height: 28, fontSize: 12 }}
        />

        <Button
          type="primary"
          loading={saving}
          onClick={addTimeline}
          style={{
            width: 60,
            height: 28,
            fontSize: 12,
            borderRadius: 5,
            background: "#5b2be0",
          }}
        >
          Add
        </Button>
      </div>

      {sorted.map((item) => (
        <div
          key={item.id}
          style={{ display: "flex", position: "relative" }}
        >
          <div
            style={{
              width: 22,
              display: "flex",
              justifyContent: "center",
            }}
          >
            <div
              style={{
                position: "absolute",
                top: 0,
                bottom: 0,
                width: 2,
                background: "#d9e4ef",
              }}
            />

            <div
              style={{
                width: 15,
                height: 15,
                marginTop: 7,
                zIndex: 1,
                borderRadius: "50%",
                background: "#0057a8",
              }}
            />
          </div>

          <Card
            style={{
              flex: 1,
              marginBottom: 6,
              borderRadius: 8,
            }}
            bodyStyle={{ padding: "6px 10px" }}
          >
            <div
              style={{
                display: "flex",
                gap: 6,
                alignItems: "center",
                marginBottom: 4,
              }}
            >
              <Text
                style={{
                  fontSize: 11,
                  color: "#0057a8",
                  fontWeight: 600,
                }}
              >
                {item.time
                  ? dayjs(item.time).format("HH:mm")
                  : "--:--"}
              </Text>

              <Tag
                style={{
                  background:
                    TIMELINE_COLOR[item.type?.toLowerCase()] ??
                    "#0057a8",
                  color: "#fff",
                  border: "none",
                  fontSize: 10,
                  padding: "0 5px",
                  lineHeight: "15px",
                  margin: 0,
                }}
              >
                {item.type?.toUpperCase()}
              </Tag>
            </div>

            <Text strong style={{ fontSize: 12 }}>
              {item.event}
            </Text>
          </Card>
        </div>
      ))}
    </div>
  );
}
// ---------------------------------------------------------------------------
// Reports tab
// ---------------------------------------------------------------------------

function ReportsTab({ patientId }: { patientId: number }) {
  const [downloading, setDownloading] = useState(false);
  const [modalTitle, setModalTitle] = useState("");
  const [modalData, setModalData] = useState<Record<string, unknown> | null>(
    null
  );
  const [modalLoading, setModalLoading] = useState(false);

  async function handleCsv() {
    try {
      setDownloading(true);
      await downloadVitalsCsv(patientId);
    } catch (err) {
      console.error("CSV download failed:", err);
      message.error("Failed to download vitals CSV");
    } finally {
      setDownloading(false);
    }
  }

  async function openReport(
    title: string,
    loader: (id: number) => Promise<Record<string, unknown>>
  ) {
    try {
      setModalTitle(title);
      setModalData(null);
      setModalLoading(true);
      const data = await loader(patientId);
      setModalData(data);
    } catch (err) {
      console.error("Report load failed:", err);
      message.error(`Failed to load ${title}`);
      setModalTitle("");
    } finally {
      setModalLoading(false);
    }
  }

  const cards = [
    {
      key: "daily",
      icon: <PrinterOutlined />,
      title: "Print Daily Summary",
      desc: "Generates a PDF of flowsheet, meds, and vitals.",
      onClick: () => openReport("Daily Summary", getDailySummaryReport),
    },
    {
      key: "csv",
      icon: downloading ? <Spin /> : <DownloadOutlined />,
      title: "Export 24h Vitals CSV",
      desc: "Download CSV of all monitored parameters.",
      onClick: handleCsv,
    },
    {
      key: "discharge",
      icon: <FileTextOutlined />,
      title: "Discharge Summary",
      desc: "Complete patient discharge document.",
      onClick: () => openReport("Discharge Summary", getDischargeSummaryReport),
    },
  ];

  return (
    <>
      <Row gutter={[16, 16]}>
        {cards.map((c) => (
          <Col xs={24} sm={12} md={8} key={c.key}>
            <Card
              hoverable
              onClick={c.onClick}
              style={{ height: "100%", cursor: "pointer" }}
              styles={{ body: { padding: 28 } }}
            >
              <div style={{ textAlign: "center" }}>
                <div
                  style={{
                    width: 56,
                    height: 56,
                    borderRadius: "50%",
                    background: "#f4f0fe",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    margin: "0 auto 14px",
                    fontSize: 24,
                    color: BRAND_PURPLE,
                  }}
                >
                  {c.icon}
                </div>
                <Title level={5} style={{ margin: "0 0 6px" }}>
                  {c.title}
                </Title>
                <Text type="secondary">{c.desc}</Text>
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      <Modal
        title={modalTitle}
        open={!!modalTitle}
        onCancel={() => setModalTitle("")}
        footer={null}
        width={720}
      >
        {modalLoading ? (
          <div style={{ textAlign: "center", padding: 32 }}>
            <Spin />
          </div>
        ) : (
          <pre
            style={{
              background: "#f5f6fa",
              padding: 16,
              borderRadius: 8,
              maxHeight: "60vh",
              overflow: "auto",
              fontSize: 12,
            }}
          >
            {JSON.stringify(modalData, null, 2)}
          </pre>
        )}
      </Modal>
    </>
  );
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

const PatientDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [details, setDetails] = useState<PatientDetails | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");

  // Live state (driven by the WebSocket stream)
  const [liveSnapshot, setLiveSnapshot] = useState<LatestVital | null>(null);
  const [liveTrend, setLiveTrend] = useState<Vital[]>([]);
  const [liveAlarmCount, setLiveAlarmCount] = useState<number | null>(null);
  const [lastUpdate, setLastUpdate] = useState<string | null>(null);
  const trendIdRef = useRef(0);
  const [open, setOpen] = useState(false);

  const patientId = id ? parseInt(id, 10) : NaN;

  async function loadDetails() {
    if (!id || isNaN(patientId)) return;
    try {
      setLoading(true);
      const data = await getPatientDetails(patientId);
      setDetails(data);
    } catch (err) {
      console.error("Failed to load patient details:", err);
      message.error("Failed to load patient details");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDetails();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  // Seed live state once per patient (not on every refetch, so the trend
  // accumulated from the socket is preserved when notes etc. reload details).
  const loadedPatientId = details?.overview.patient.id;
  useEffect(() => {
    if (details) {
      setLiveSnapshot(details.overview.latestVitals ?? null);
      setLiveTrend(details.vitals ?? []);
      setLiveAlarmCount(details.overview.activeAlarmCount ?? 0);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loadedPatientId]);

  // Subscribe to the unit-scoped live-vitals WebSocket for this patient.
  useLiveVitals(
    details?.overview.unitId,
    (msg) => {
      if (msg.patient_id !== patientId) return;
      const s = msg.snapshot;
      const num = (v: number | null) => (v === null ? undefined : v);
      setLiveSnapshot({
        patientId: msg.patient_id,
        bedId: msg.bed_id,
        hr: num(s.hr),
        bpSys: num(s.bp_sys),
        bpDia: num(s.bp_dia),
        spo2: num(s.spo2),
        temp: num(s.temp),
        rr: num(s.rr),
        status: s.status ?? undefined,
        recordedAt: msg.recorded_at,
      });
      setLiveTrend((prev) => {
        const next = [
          ...prev,
          {
            id: --trendIdRef.current,
            patientId: msg.patient_id,
            hr: num(s.hr),
            bpSys: num(s.bp_sys),
            bpDia: num(s.bp_dia),
            spo2: num(s.spo2),
            temp: num(s.temp),
            rr: num(s.rr),
            recordedAt: msg.recorded_at,
          },
        ];
        return next.slice(-240);
      });
      setLastUpdate(msg.recorded_at);
    },
    (alarm) => {
      if (alarm.patient_id === patientId) {
        setLiveAlarmCount((c) => (c ?? 0) + 1);
      }
    }
  );

  if (loading && !details) {
    return (
      <div style={{ padding: 40, textAlign: "center" }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!details) {
    return (
      <div style={{ padding: 24 }}>
        <Button onClick={() => navigate(-1)} style={{ marginBottom: 16 }}>
          ← Back
        </Button>
        <Empty description="Patient not found" />
      </div>
    );
  }

  const patient = details.overview.patient;
  const staff: StaffAssignment[] = details.staffAssignment ?? [];

  const tabItems = [
    {
      key: "overview",
      label: "Overview",
      children: (
        <OverviewTab
          patient={patient}
          vitals={liveTrend.length ? liveTrend : details.vitals ?? []}
          latestVitals={liveSnapshot ?? details.overview.latestVitals}
          ventilator={details.ventilatorParams}
          lab={details.labData}
          fluid={details.fluidBalance}
          unitId={details.overview.unitId}
          lastUpdate={lastUpdate}
        />
      ),
    },
    {
      key: "flowsheet",
      label: "Flowsheet",
      children: <FlowsheetTab patientId={patientId} />,
    },
    {
      key: "devices",
      label: `Devices (${details.devices?.length ?? 0})`,
      children: <DevicesTab devices={details.devices ?? []} />,
    },
    {
      key: "medication",
      label: `Medication (${details.medications?.length ?? 0})`,
      children: <MedicationTab medications={details.medications ?? []} />,
    },
    {
      key: "notes",
      label: `Notes (${details.notes?.length ?? 0})`,
      children: (
        <NotesTab
          patientId={patientId}
          notes={details.notes ?? []}
          onChanged={loadDetails}
        />
      ),
    },
    {
      key: "timeline",
      label: "Timeline",
      children: <TimelineTab events={details.timeline ?? []} patientId={patientId} />,
    },
    {
      key: "reports",
      label: "Reports",
      children: <ReportsTab patientId={patientId} />,
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      {/* Patient header */}
      <div style={{ marginBottom: 18 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 16 }}>
          <Button onClick={() => navigate(-1)} style={{ width: 40, height: 40, borderRadius: 12, fontSize: 18 }}>
            ←</Button>
          <Title level={2} style={{ margin: 0, fontSize: 18, fontWeight: 700, letterSpacing: 1, color: "#0f172a" }}>{patient.name}</Title>
          <span style={{ background: "#e8f2ff", color: "#0050b3", padding: "8px 18px", borderRadius: 6, fontWeight: 700, fontSize: 14 }}>{patient.bedId}</span></div>
        <div style={{ display: "flex", alignItems: "center", gap: 22, fontSize: 12, color: "#0f172a" }}>
          <span>{patient.age} yrs / {patient.gender}</span>{staff.length > 0 && <span>♙ {staff[0].staffName}</span>}
          <span>Diagnosis: {patient.diagnosis}</span>
          <div
            onClick={() => setOpen(true)}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              color: "#0d9488",
              cursor: "pointer",
              marginTop: "8px"
            }}
          >
            <Info size={16} />
            <span
              style={{
                fontSize: "14px",
                fontWeight: 500
              }}
            >
              More Info
            </span>
          </div>
          {open && (
            <PatientModal patient={patient} onClose={() => setOpen(false)} />
          )}
        </div></div>

      <Tabs activeKey={activeTab} onChange={setActiveTab} items={tabItems} className="patient-tabs" />
    </div>
  );
};

export default PatientDetailPage;
