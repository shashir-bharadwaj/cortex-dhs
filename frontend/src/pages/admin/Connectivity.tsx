import React, { useEffect, useState } from "react";
import { Table, Tag } from "antd";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Wifi, WifiOff, Activity, Clock } from "lucide-react";
import {
  getConnectivityStatus,
  type ConnectivitySummary,
  type ConnectivityTimeline,
  type ConnectivityDevice,
} from "../../api/adminApi";

const getStatusTag = (status: string) => {
  if (status === "Online") return <Tag color="green">● Online</Tag>;
  if (status === "Offline") return <Tag>● Offline</Tag>;
  return <Tag color="red">● Error</Tag>;
};

const defaultSummary: ConnectivitySummary = {
  online: 0,
  offline: 0,
  dataRate: "--",
  latency: "--",
};

const ConnectivityPage = () => {
  const [summary, setSummary] = useState<ConnectivitySummary>(defaultSummary);
  const [timeline, setTimeline] = useState<ConnectivityTimeline[]>([]);
  const [devices, setDevices] = useState<ConnectivityDevice[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    const loadConnectivity = async () => {
      try {
        const response = await getConnectivityStatus();
        if (mounted) {
          setSummary(response.summary || defaultSummary);
          setTimeline(response.timeline || []);
          setDevices(response.devices || []);
        }
      } catch (error) {
        console.error("Failed to load connectivity data", error);
        if (mounted) {
          setSummary(defaultSummary);
          setTimeline([]);
          setDevices([]);
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadConnectivity();

    return () => {
      mounted = false;
    };
  }, []);

  const columns = [
    { title: "Device", dataIndex: "id" },
    { title: "Type", dataIndex: "type" },
    {
      title: "Bed",
      dataIndex: "bed",
      render: (t: string) => <b>{t}</b>,
    },
    {
      title: "Status",
      dataIndex: "status",
      render: (s: string) => getStatusTag(s),
    },
    { title: "Last Sync", dataIndex: "lastSync" },
    { title: "IP", dataIndex: "ip" },
  ];

  return (
    <div style={{ padding: 24, display: "flex", flexDirection: "column", gap: 24 }}>
      <div>
        <h2 style={{ fontSize: 24, fontWeight: 600 }}>Connectivity Monitoring</h2>
        <p style={{ color: "#6b7280" }}>
          Network health and device connectivity status
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 16 }}>
        <div style={{ background: "#22c55e", color: "#fff", borderRadius: 12, padding: 20, display: "flex", justifyContent: "space-between", alignItems: "center", boxShadow: "0 2px 8px rgba(0,0,0,.15)" }}>
          <div>
            <p style={{ fontSize: 14, opacity: 0.8 }}>ONLINE</p>
            <h3 style={{ fontSize: 24, fontWeight: 700 }}>{loading ? "--" : summary.online}</h3>
          </div>
          <Wifi style={{ width: 24, height: 24, opacity: 0.8 }} />
        </div>

        <div style={{ background: "#f97316", color: "#fff", borderRadius: 12, padding: 20, display: "flex", justifyContent: "space-between", alignItems: "center", boxShadow: "0 2px 8px rgba(0,0,0,.15)" }}>
          <div>
            <p style={{ fontSize: 14, opacity: 0.8 }}>OFFLINE</p>
            <h3 style={{ fontSize: 24, fontWeight: 700 }}>{loading ? "--" : summary.offline}</h3>
          </div>
          <WifiOff style={{ width: 24, height: 24, opacity: 0.8 }} />
        </div>

        <div style={{ background: "#fff", borderRadius: 12, padding: 20, display: "flex", justifyContent: "space-between", alignItems: "center", boxShadow: "0 2px 8px rgba(0,0,0,.15)" }}>
          <div>
            <p style={{ fontSize: 14, color: "#6b7280" }}>DATA RATE</p>
            <h3 style={{ fontSize: 20, fontWeight: 600 }}>{loading ? "--" : summary.dataRate}</h3>
          </div>
          <Activity style={{ width: 24, height: 24, color: "#9ca3af" }} />
        </div>

        <div style={{ background: "#fff", borderRadius: 12, padding: 20, display: "flex", justifyContent: "space-between", alignItems: "center", boxShadow: "0 2px 8px rgba(0,0,0,.15)" }}>
          <div>
            <p style={{ fontSize: 14, color: "#6b7280" }}>LATENCY</p>
            <h3 style={{ fontSize: 20, fontWeight: 600 }}>{loading ? "--" : summary.latency}</h3>
          </div>
          <Clock style={{ width: 24, height: 24, color: "#9ca3af" }} />
        </div>
      </div>

      <div style={{ background: "#fff", borderRadius: 12, padding: 20, boxShadow: "0 2px 8px rgba(0,0,0,.15)" }}>
        <h3 style={{ fontWeight: 600, marginBottom: 16 }}>Real-Time Connectivity Timeline</h3>

        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={timeline}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="online" stroke="#22c55e" strokeWidth={2} />
            <Line type="monotone" dataKey="offline" stroke="#ef4444" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{ background: "#fff", borderRadius: 12, padding: 20, boxShadow: "0 2px 8px rgba(0,0,0,.15)" }}>
        <Table columns={columns} dataSource={devices} rowKey="id" pagination={false} />
      </div>
    </div>
  );
};

export default ConnectivityPage;
