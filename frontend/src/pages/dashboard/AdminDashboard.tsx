import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";
import {
  Building2,
  Bed,
  Users,
  Wifi,
  WifiOff,
  AlertTriangle,
  Plus,
} from "lucide-react";
import { getAdminDashboardOverview, type AdminDashboardOverviewResponse } from "../../api/adminApi";

const DashboardPageAdmin = () => {
  const [dashboardData, setDashboardData] = useState<AdminDashboardOverviewResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    const loadDashboard = async () => {
      try {
        const data = await getAdminDashboardOverview();
        if (isMounted) {
          setDashboardData(data);
        }
      } catch (error) {
        console.error("Failed to load admin dashboard overview", error);
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadDashboard();

    return () => {
      isMounted = false;
    };
  }, []);

  const stats = dashboardData?.stats ?? {
    hospitals: 0,
    icuUnits: 0,
    beds: 0,
    connected: 0,
    offline: 0,
    patients: 0,
    critical: 0,
  };
  const connectivityTrend = dashboardData?.connectivityTrend ?? [];
  const alertsData = dashboardData?.alertsData ?? [];
  const liveAlerts = dashboardData?.liveAlerts ?? [];

  if (loading) {
    return (
      <div style={{ padding: 16 }}>
        <p style={{ color: "#6b7280" }}>Loading dashboard overview...</p>
      </div>
    );
  }

  return (
    <div style={{ padding: 16, display: "flex", flexDirection: "column", gap: 16 }}> {/* tailwind: p-4 space-y-4 */}

      <div style={{ display: "flex", justifyContent: "space-between" }}> {/* tailwind: flex justify-between */}
        <div>
          <h2 style={{ fontSize: 20, fontWeight: 600 }}>Dashboard</h2> {/* tailwind: text-xl font-semibold */}
          <p style={{ color: "#6b7280", fontSize: 13 }}>Real-time ICU monitoring overview</p> {/* tailwind: text-gray-500 text-sm */}
        </div>

        <div style={{ backgroundColor: "#dcfce7", color: "#16a34a", padding: "4px 12px", borderRadius: 999, fontSize: 14 }}> {/* tailwind: bg-green-100 text-green-600 px-3 py-1 rounded-full text-sm */}
          Live
        </div>
      </div>

      {/* ================= STATS ================= */}

      <div style={{ display: "grid", gridTemplateColumns: "repeat(7,1fr)", gap: 12 }}> {/* tailwind: grid grid-cols-2 md:grid-cols-7 gap-3 */}
        <StatCard title="HOSPITALS" value={stats.hospitals} icon={<Building2 />} />
        <StatCard title="ICU UNITS" value={stats.icuUnits} icon={<Building2 />} />
        <StatCard title="TOTAL BEDS" value={stats.beds} icon={<Bed />} />

        <StatCard colored title="CONNECTED" value={stats.connected} icon={<Wifi />} color="#22c55e" />
        <StatCard colored title="OFFLINE" value={stats.offline} icon={<WifiOff />} color="#f97316" />
        <StatCard colored title="PATIENTS" value={stats.patients} icon={<Users />} color="#14b8a6" />
        <StatCard colored title="CRITICAL" value={stats.critical} icon={<AlertTriangle />} color="#ef4444" />
      </div>


      {/* ================= CHARTS ================= */}

      <div style={{ display: "grid", gridTemplateColumns: "repeat(2,1fr)", gap: 12 }}> {/* tailwind: grid md:grid-cols-2 gap-3 */}

        <Card>
          <h3 style={{ fontWeight: 600, fontSize: 14, marginBottom: 12 }}>Device Connectivity Trend</h3> {/* tailwind: font-semibold text-sm mb-3 */}

          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={connectivityTrend}>
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Line dataKey="online" stroke="#22c55e" />
              <Line dataKey="offline" stroke="#ef4444" />
            </LineChart>
          </ResponsiveContainer>
        </Card>


        <Card>
          <h3 style={{ fontWeight: 600, fontSize: 14, marginBottom: 12 }}>Bed Occupancy Rate</h3> {/* tailwind: font-semibold text-sm mb-3 */}

          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={alertsData}>
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="critical" fill="#ef4444" />
              <Bar dataKey="warning" fill="#f59e0b" />
              <Bar dataKey="info" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </Card>

      </div>


      {/* ================= ALERTS ================= */}

      <div style={{ display: "grid", gridTemplateColumns: "repeat(2,1fr)", gap: 12 }}> {/* tailwind: grid md:grid-cols-2 gap-3 */}

        <Card>
          <h3 style={{ fontWeight: 600, fontSize: 14, marginBottom: 12 }}>Alerts (Last 24h)</h3>

          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={alertsData}>
              <XAxis dataKey="time" />
              <YAxis />
              <Bar dataKey="critical" fill="#ef4444" />
              <Bar dataKey="warning" fill="#f59e0b" />
              <Bar dataKey="info" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>

        </Card>


        <Card>

          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 12 }}> {/* tailwind: flex justify-between mb-3 */}
            <h3 style={{ fontWeight: 600, fontSize: 14 }}>Live Alerts</h3>
            <span style={{ color: "#ef4444", fontSize: 14 }}>● 4 Active</span>
          </div>


          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}> {/* tailwind: space-y-3 */}

            {liveAlerts.map((a, i) => (
              <div
                key={i}
                style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 12, display: "flex", justifyContent: "space-between" }}
              > {/* tailwind: border rounded-lg p-3 flex justify-between */}

                <div>
                  <p style={{ fontWeight: 600 }}>{a.bed}</p>
                  <p style={{ color: "#6b7280", fontSize: 14 }}>{a.message}</p>
                </div>

                <span style={{ color: "#9ca3af", fontSize: 14 }}>
                  {a.time}
                </span>

              </div>
            ))}

          </div>

        </Card>

      </div>


      {/* <Card>

        <h3 style={{ fontWeight: 600, fontSize: 14, marginBottom: 12 }}>Quick Actions</h3>

        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <ActionBtn label="Add ICU" primary />
          <ActionBtn label="Add Bed" />
          <ActionBtn label="Register Device" />
          <ActionBtn label="Create User" />
        </div>

      </Card> */}

    </div>
  );
};


/* ================= SMALL COMPONENTS ================= */


const Card = ({ children }: any) => (
  <div style={{ backgroundColor: "white", borderRadius: 12, boxShadow: "0 2px 8px #ddd", padding: 16 }}> {/* tailwind: bg-white rounded-xl shadow p-4 */}
    {children}
  </div>
);


const StatCard = ({ title, value, icon, colored, color }: any) => (
  <div
    style={{
      borderRadius: 12,
      padding: 12,
      boxShadow: "0 2px 8px #ddd",
      display: "flex",
      justifyContent: "space-between",
      backgroundColor: colored ? color : "white",
      color: colored ? "white" : "black",
    }}
  > {/* tailwind: rounded-xl p-4 shadow flex justify-between */}

    <div>
      <p style={{ fontSize: 11, opacity: .8 }}>{title}</p>
      <h3 style={{ fontSize: 18, fontWeight: 700 }}>{value}</h3>
    </div>

    <div style={{ opacity: .8 }}>
      {icon}
    </div>

  </div>
);


const ActionBtn = ({ label, primary }: any) => (
  <button
    style={{
      padding: "8px 16px",
      borderRadius: 8,
      border: "1px solid #ddd",
      backgroundColor: primary ? "#14b8a6" : "#f3f4f6",
      color: primary ? "white" : "#374151",
    }}
  > {/* tailwind: px-4 py-2 rounded-lg border */}

    {primary && <Plus style={{ width: 16, marginRight: 8 }} />}
    {label}

  </button>
);


export default DashboardPageAdmin;