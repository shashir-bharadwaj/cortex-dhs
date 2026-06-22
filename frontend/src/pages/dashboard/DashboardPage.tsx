import React, { useEffect, useState, useCallback, useRef } from "react";
import {
  Row,
  Col,
  Card,
  Statistic,
  Tabs,
  Tag,
  Spin,
  message,
  Badge,
  Tooltip,
  Empty,
} from "antd";
import {
  HeartOutlined,
  AlertOutlined,
  WarningOutlined,
  CheckCircleOutlined,
  ThunderboltOutlined,
  UserOutlined,
  ExperimentOutlined,
  DashboardOutlined,
  FireOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { getDashboardUnits, getDashboardOverview } from "../../api/dashboardApi";
import { ICUUnitMaster, DashboardOverview, PatientCard, VitalReading } from "../../types/dashboard";
import "./DashboardPage.css";

const POLL_INTERVAL_MS = 5000;

const STATUS_COLOR: Record<string, string> = {
  critical: "#ff4d4f",
  warning: "#fa8c16",
  normal: "#52c41a",
};

// Minimal ECG waveform icon
function EcgIcon({ color = "#bbb" }: { color?: string }) {
  return (
    <svg width="22" height="10" viewBox="0 0 44 20" fill="none">
      <polyline
        points="0,10 8,10 11,2 14,18 17,4 20,16 23,10 44,10"
        stroke={color}
        strokeWidth="2.2"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
    </svg>
  );
}

// Simple decorative sparkline
function TrendLine({ color = "#e0e0e0" }: { color?: string }) {
  return (
    <svg width="100%" height="10" viewBox="0 0 80 18" preserveAspectRatio="none">
      <polyline
        points="0,12 12,9 22,11 34,6 44,10 56,8 68,11 80,9"
        stroke={color}
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
        opacity="0.6"
      />
    </svg>
  );
}

function VitalBox({
  icon,
  label,
  unit,
  reading,
  showTrend = false,
}: {
  icon: React.ReactNode;
  label: string;
  unit: string;
  reading?: VitalReading | null;
  showTrend?: boolean;
}) {
  const statusKey = reading?.status?.toLowerCase() ?? "normal";
  const isCritical = statusKey === "critical";
  const isWarning = statusKey === "warning";
  const valueColor = isCritical ? "#ff4d4f" : isWarning ? "#fa8c16" : "#1a1a2e";
  const trendColor = isCritical ? "#ffb3b3" : isWarning ? "#ffd591" : "#d9d9d9";

  return (
    <div style={{
      flex: 1,
      background: "#eef1f4",
      borderRadius: 8,
      padding: "8px 12px",
      minHeight: 58,
    }}>
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        marginBottom: 6,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 4 }}>
          <span style={{ color: isCritical ? "#ff4d4f" : "#aaa", fontSize: 12 }}>
            {icon}
          </span>

          <span style={{ fontSize: 9, color: "#0f172a", fontWeight: 500 }}>
            {label}
          </span>
        </div>
        <span style={{ fontSize: 9, color: "#0f172a" }}>{unit}</span>
      </div>
      <div style={{ fontSize: 13, fontWeight: 700, color: "#0f172a", lineHeight: 1 }}>
        {reading?.value ?? "—"}
      </div>
      {showTrend && <TrendLine color={trendColor} />}
    </div>
  );
}

function PatientCardItem({
  card,
  onClick,
}: {
  card: PatientCard;
  onClick?: () => void;
}) {
  const statusKey = (card.status ?? "normal").toLowerCase();
  const isCritical = statusKey === "critical";
  const isWarning = statusKey === "warning";
  const patient = card.patient;
  const isClickable = !!patient && !!onClick;
  const ecgColor = isCritical ? "#ff4d4f" : isWarning ? "#fa8c16" : "#bbb";

  const cardClassName = isCritical
    ? "patient-card-critical"
    : isWarning
      ? "patient-card-warning"
      : "patient-card-normal";

  return (
    <div
      className={cardClassName}
      onClick={isClickable ? onClick : undefined}
      style={{
        borderRadius: 10,
        padding: "10px 12px",
        cursor: isClickable ? "pointer" : "default",
        transition: "transform 0.15s",
        height: "100%",
        boxSizing: "border-box",
      }}
      onMouseEnter={(e) => {
        if (isClickable) (e.currentTarget as HTMLDivElement).style.transform = "translateY(-2px)";
      }}
      onMouseLeave={(e) => {
        (e.currentTarget as HTMLDivElement).style.transform = "translateY(0)";
      }}
    >
      {/* Top row: Bed ID + status badge + ECG icon */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 8 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <span
            style={{
              fontSize: 11,
              fontWeight: 600,
              color: "#555",
              background: "#f0f0f0",
              borderRadius: 4,
              padding: "1px 7px",
            }}
          >
            {card.bed.bedId}
          </span>

          {isCritical && (
            <span
              style={{
                display: "flex",
                alignItems: "center",
                gap: 3,
                background: "#ff4d4f",
                color: "#fff",
                fontSize: 10,
                fontWeight: 700,
                borderRadius: 4,
                padding: "1px 6px",
              }}
            >
              <AlertOutlined style={{ fontSize: 9 }} />
              CRITICAL
            </span>
          )}
          {isWarning && (
            <span
              style={{
                display: "flex",
                alignItems: "center",
                gap: 3,
                background: "#fa8c16",
                color: "#fff",
                fontSize: 10,
                fontWeight: 700,
                borderRadius: 4,
                padding: "1px 6px",
              }}
            >
              <WarningOutlined style={{ fontSize: 9 }} />
              WARNING
            </span>
          )}
        </div>

        {card.hasCriticalAlarm ? (
          <Tooltip title={`${card.activeAlarmCount} active alarm(s)`}>
            <Badge count={card.activeAlarmCount} size="small" offset={[-2, 2]}>
              <EcgIcon color={ecgColor} />
            </Badge>
          </Tooltip>
        ) : (
          <EcgIcon color={ecgColor} />
        )}
      </div>

      {patient ? (
        <>
          {/* Patient name + demographics */}
          <div style={{ marginBottom: 6 }}>
            <div style={{ fontWeight: 700, fontSize: 14, color: "#1a1a2e", lineHeight: 1.2 }}>
              {patient.name}
            </div>
            <div style={{ fontSize: 11, color: "#777", marginTop: 2 }}>
              {[
                patient.age ? `${patient.age}y` : null,
                patient.gender ? (patient.gender === "MALE" ? "M" : patient.gender === "FEMALE" ? "F" : patient.gender) : null,
                patient.diagnosis,
              ]
                .filter(Boolean)
                .join(" · ")}
            </div>
          </div>

          {patient.doctor && (
            <div style={{ display: "flex", alignItems: "center", gap: 4, marginBottom: 10, fontSize: 11, color: "#888" }}>
              <UserOutlined style={{ fontSize: 10 }} />
              {patient.doctor}
            </div>
          )}

          {/* Vitals grid */}
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 10,
              marginBottom: 8,
            }}
          >
            {/* Row 1: HR | SPO2 */}
            <div style={{ display: "flex", gap: 10 }}>
              <VitalBox
                icon={<HeartOutlined />}
                label="HR"
                unit="bpm"
                reading={card.vitals?.hr}
                showTrend
              />
              <div style={{ width: 1, background: "#f0f0f0" }} />
              <VitalBox
                icon={<ExperimentOutlined />}
                label="SPO2"
                unit="%"
                reading={card.vitals?.spo2}
                showTrend
              />
            </div>

            {/* Row 2: BP | RR */}
            <div style={{ display: "flex", gap: 10 }}>
              <VitalBox
                icon={<DashboardOutlined />}
                label="BP"
                unit="mmHg"
                reading={card.vitals?.bp}
              />
              <div style={{ width: 1, background: "#f0f0f0" }} />
              <VitalBox
                icon={<DashboardOutlined />}
                label="RR"
                unit="/min"
                reading={card.vitals?.rr}
              />
            </div>

            {/* Row 3: TEMP full width */}
            <div
              style={{
                background: "#eef1f4",
                borderRadius: 8,
                padding: "8px 12px",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 4 }}>
                <FireOutlined style={{ fontSize: 12, color: "#ff7a45" }}
                />
                <span style={{ fontSize: 10, color: "#999", fontWeight: 500 }}>TEMP</span>
              </div>
              <span
                style={{
                  fontSize: 14,
                  fontWeight: 700,
                  color:
                    card.vitals?.temp?.status?.toLowerCase() === "critical"
                      ? "#ff4d4f"
                      : card.vitals?.temp?.status?.toLowerCase() === "warning"
                        ? "#fa8c16"
                        : "#1a1a2e",
                }}
              >
                {card.vitals?.temp?.value != null
                  ? `${card.vitals.temp.value}${card.vitals.temp.unit}`
                  : "—"}
              </span>
            </div>
          </div>

          {/* Monitoring tags */}
          {card.monitoring.length > 0 && (
            <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
              {card.monitoring.map((m) => (
                <span
                  key={m}
                  style={{
                    fontSize: 9,
                    fontWeight: 600,
                    background: isCritical ? "#ffe0e0" : "#e8f4ff",
                    color: isCritical ? "#cf1322" : "#1677ff",
                    borderRadius: 3,
                    padding: "1px 5px",
                    border: `1px solid ${isCritical ? "#ffb3b3" : "#bae0ff"}`,
                  }}
                >
                  {m}
                </span>
              ))}
            </div>
          )}
        </>
      ) : (
        <div style={{ color: "#bbb", fontSize: 12, paddingTop: 8 }}>Bed available</div>
      )}
    </div>
  );
}

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [units, setUnits] = useState<ICUUnitMaster[]>([]);
  const [selectedUnitId, setSelectedUnitId] = useState<number | null>(null);
  const [overview, setOverview] = useState<DashboardOverview | null>(null);
  const [loadingUnits, setLoadingUnits] = useState(true);
  const [loadingOverview, setLoadingOverview] = useState(false);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    async function fetchUnits() {
      try {
        const data = await getDashboardUnits();
        setUnits(data);
        if (data.length > 0) setSelectedUnitId(data[0].id);
      } catch {
        message.error("Failed to load ICU units");
      } finally {
        setLoadingUnits(false);
      }
    }
    fetchUnits();
  }, []);

  const refreshOverview = useCallback(async (unitId: number, showSpinner = false) => {
    if (showSpinner) setLoadingOverview(true);
    try {
      const data = await getDashboardOverview(unitId);
      setOverview(data);
    } catch {
      // silent poll errors
    } finally {
      if (showSpinner) setLoadingOverview(false);
    }
  }, []);

  useEffect(() => {
    if (selectedUnitId == null) return;
    refreshOverview(selectedUnitId, true);

    if (pollRef.current) clearInterval(pollRef.current);
    pollRef.current = setInterval(() => refreshOverview(selectedUnitId, false), POLL_INTERVAL_MS);

    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, [selectedUnitId, refreshOverview]);

  const summary = overview?.summary;

  const statsCards = [
    {
      title: "Total Beds",
      value: overview?.unit.totalBeds ?? "—",
      icon: <CheckCircleOutlined style={{ fontSize: 22, color: "#1890ff" }} />,
      color: "#e6f7ff",
      border: "#1890ff",
    },
    {
      title: "Occupied",
      value: overview?.unit.occupiedBeds ?? "—",
      icon: <HeartOutlined style={{ fontSize: 22, color: "#52c41a" }} />,
      color: "#f6ffed",
      border: "#52c41a",
    },
    {
      title: "Critical",
      value: summary?.critical ?? "—",
      icon: <AlertOutlined style={{ fontSize: 22, color: "#ff4d4f" }} />,
      color: "#fff1f0",
      border: "#ff4d4f",
    },
    {
      title: "Warnings",
      value: summary?.warning ?? "—",
      icon: <WarningOutlined style={{ fontSize: 22, color: "#fa8c16" }} />,
      color: "#fff7e6",
      border: "#fa8c16",
    },

  ];

  const tabItems = units.map((u) => ({
    key: String(u.id),
    label: u.icu_name,
  }));

  return (
    <div style={{ padding: "24px 28px", background: "#f5f6fa", minHeight: "100vh" }}>
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ margin: 0, fontSize: 20, fontWeight: 700, color: "#1a1a2e" }}>
          ICU OverView
        </h2>
        <span style={{ color: "#888", fontSize: 13 }}>
          Real-time patient monitoring · auto-refreshes every {POLL_INTERVAL_MS / 1000}s
        </span>
      </div>

      {/* Stats Row */}
      <Row gutter={[16, 16]} style={{ marginBottom: 20 }}>
        {statsCards.map((s) => (
          <Col key={s.title} xs={24} sm={12} md={6} lg={6} xl={6}>
            <Card
              style={{
                borderRadius: 10,
                background: s.color,
                border: `1px solid ${s.border}30`,
                boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
              }}
              bodyStyle={{ padding: "14px 18px" }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                <div
                  style={{
                    background: "#fff",
                    borderRadius: 8,
                    padding: 8,
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  {s.icon}
                </div>
                <Statistic
                  title={<span style={{ fontSize: 11, color: "#666" }}>{s.title}</span>}
                  value={s.value}
                  valueStyle={{ fontSize: 22, fontWeight: 700, color: "#1a1a2e" }}
                />
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      {/* Unit Tabs + Patient Grid */}
      {loadingUnits ? (
        <Spin />
      ) : (
        <Card
          style={{ borderRadius: 10, boxShadow: "0 2px 8px rgba(0,0,0,0.06)" }}
          bodyStyle={{ padding: 0 }}
        >
          <div style={{ padding: "0 20px", borderBottom: "1px solid #f0f0f0" }}>
            <Tabs
              activeKey={selectedUnitId ? String(selectedUnitId) : undefined}
              onChange={(key) => setSelectedUnitId(Number(key))}
              items={tabItems}
              tabBarStyle={{ marginBottom: 0 }}
            />
          </div>

          <div style={{ padding: "20px 20px" }}>
            {loadingOverview ? (
              <div style={{ textAlign: "center", padding: "60px 0" }}>
                <Spin size="large" />
              </div>
            ) : overview?.patientCards.length === 0 ? (
              <Empty description="No beds in this unit" />
            ) : (
              <Row gutter={[12, 12]}>
                {overview?.patientCards.map((card) => (
                  <Col key={card.bed.id} xs={24} sm={12} md={12} lg={8} xl={6}>
                    <PatientCardItem
                      card={card}
                      onClick={
                        card.patient
                          ? () => navigate(`/patients/${card.patient!.id}`)
                          : undefined
                      }
                    />
                  </Col>
                ))}
              </Row>
            )}
          </div>
        </Card>
      )}
    </div>
  );
};

export default DashboardPage;
