import React from "react";
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
import {
  Wifi,
  WifiOff,
  Activity,
  Clock,
} from "lucide-react";
import { useConnectivity } from "../../context/connectivityContext";


const getStatusTag = (status: string) => {
  if (status === "Online")
    return <Tag color="green">● Online</Tag>;
  if (status === "Offline")
    return <Tag>● Offline</Tag>;
  return <Tag color="red">● Error</Tag>;
};


const ConnectivityPage = () => {
  const { summary, timeline, devices } = useConnectivity();

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

        {/* Header */}
        <div>
          <h2 style={{ fontSize: 24, fontWeight: 600 }}>
            Connectivity Monitoring
          </h2>

          {/* tailwind: text-gray-500 */}
          <p style={{ color: "#6b7280" }}>
            Network health and device connectivity status
          </p>
        </div>

        {/* tailwind: grid grid-cols-1 md:grid-cols-4 gap-4 */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 16 }}>

          {/* Online */}
          {/* tailwind: bg-green-500 text-white rounded-xl p-5 flex justify-between items-center shadow */}
          <div style={{ background: "#22c55e", color: "#fff", borderRadius: 12, padding: 20, display: "flex", justifyContent: "space-between", alignItems: "center", boxShadow: "0 2px 8px rgba(0,0,0,.15)" }}>
            <div>
              {/* tailwind: text-sm opacity-80 */}
              <p style={{ fontSize: 14, opacity: .8 }}>ONLINE</p>
              {/* tailwind: text-2xl font-bold */}
              <h3 style={{ fontSize: 24, fontWeight: 700 }}>{summary.online}</h3>
            </div>
            {/* tailwind: w-6 h-6 opacity-80 */}
            <Wifi style={{ width: 24, height: 24, opacity: .8 }} />
          </div>

          {/* Offline */}
          {/* tailwind: bg-orange-500 text-white rounded-xl p-5 flex justify-between items-center shadow */}
          <div style={{ background: "#f97316", color: "#fff", borderRadius: 12, padding: 20, display: "flex", justifyContent: "space-between", alignItems: "center", boxShadow: "0 2px 8px rgba(0,0,0,.15)" }}>
            <div>
              {/* tailwind: text-sm opacity-80 */}
              <p style={{ fontSize: 14, opacity: .8 }}>OFFLINE</p>
              {/* tailwind: text-2xl font-bold */}
              <h3 style={{ fontSize: 24, fontWeight: 700 }}>{summary.offline}</h3>
            </div>
            {/* tailwind: w-6 h-6 opacity-80 */}
            <WifiOff style={{ width: 24, height: 24, opacity: .8 }} />
          </div>

          {/* Data Rate */}
          {/* tailwind: bg-white rounded-xl p-5 flex justify-between items-center shadow */}
          <div style={{ background: "#fff", borderRadius: 12, padding: 20, display: "flex", justifyContent: "space-between", alignItems: "center", boxShadow: "0 2px 8px rgba(0,0,0,.15)" }}>
            <div>
              {/* tailwind: text-sm text-gray-500 */}
              <p style={{ fontSize: 14, color: "#6b7280" }}>DATA RATE</p>
              {/* tailwind: text-xl font-semibold */}
              <h3 style={{ fontSize: 20, fontWeight: 600 }}>{summary.dataRate}</h3>
            </div>
            {/* tailwind: w-6 h-6 text-gray-400 */}
            <Activity style={{ width: 24, height: 24, color: "#9ca3af" }} />
          </div>

          {/* Latency */}
          {/* tailwind: bg-white rounded-xl p-5 flex justify-between items-center shadow */}
          <div style={{ background: "#fff", borderRadius: 12, padding: 20, display: "flex", justifyContent: "space-between", alignItems: "center", boxShadow: "0 2px 8px rgba(0,0,0,.15)" }}>
            <div>
              {/* tailwind: text-sm text-gray-500 */}
              <p style={{ fontSize: 14, color: "#6b7280" }}>LATENCY</p>
              {/* tailwind: text-xl font-semibold */}
              <h3 style={{ fontSize: 20, fontWeight: 600 }}>{summary.latency}</h3>
            </div>
            {/* tailwind: w-6 h-6 text-gray-400 */}
            <Clock style={{ width: 24, height: 24, color: "#9ca3af" }} />
          </div>

        </div>

        {/* ================= CHART ================= */}
        {/* tailwind: bg-white rounded-xl p-5 shadow */}
        <div style={{ background: "#fff", borderRadius: 12, padding: 20, boxShadow: "0 2px 8px rgba(0,0,0,.15)" }}>
          {/* tailwind: font-semibold mb-4 */}
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

        {/* ================= TABLE ================= */}
        {/* tailwind: bg-white rounded-xl p-5 shadow */}
        <div style={{ background: "#fff", borderRadius: 12, padding: 20, boxShadow: "0 2px 8px rgba(0,0,0,.15)" }}>
          <Table
            columns={columns}
            dataSource={devices}
            rowKey="id"
            pagination={false}
          />
        </div>

      </div>
  );
};

export default ConnectivityPage;
