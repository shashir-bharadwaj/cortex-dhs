import React, { useEffect, useState } from "react";
import { Card, Row, Col, Typography, Button } from "antd";
import { DownloadOutlined } from "@ant-design/icons";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { getReports, ReportCardsResponse, IcuDataResponse, AlertDataResponse } from "../../api/adminApi";

const { Title, Text } = Typography;

const COLORS = ["#1677ff", "#13c2c2", "#52c41a", "#ff4d4f", "#faad14"];

const ReportsPage = () => {
  const [reportCards, setReportCards] = useState<ReportCardsResponse[]>([]);
  const [icuData, setIcuData] = useState<IcuDataResponse[]>([]);
  const [alertData, setAlertData] = useState<AlertDataResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getReports()
      .then((data) => {
        setReportCards(data.reportCards);
        setIcuData(data.icuData);
        setAlertData(data.alertData);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ padding: 24 }}>
      {/* Header */}
      <Title level={3}>Reports & Analytics</Title>
      <Text type="secondary">
        Generate and view system reports
      </Text>

      
      <div style={{ marginTop: 20, marginBottom: 16 }}>
        <Button
          type="primary"
          loading={loading}
          onClick={() => {
            setLoading(true);
            getReports()
              .then((data) => {
                setReportCards(data.reportCards);
                setIcuData(data.icuData);
                setAlertData(data.alertData);
              })
              .finally(() => setLoading(false));
          }}
        >
          Refresh Reports
        </Button>
      </div>

      <Row gutter={[16, 16]} style={{ marginTop: 20 }}>
        {reportCards.map((item, i) => (
          <Col span={8} key={i}>
            <Card style={{ borderRadius: 12 }} loading={loading && reportCards.length === 0} actions={[<DownloadOutlined key="download" />]}>
              <Title level={5}>{item.title}</Title>
              <Text type="secondary">{item.desc}</Text>
            </Card>
          </Col>
        ))}
      </Row>

      <Row gutter={16} style={{ marginTop: 20 }}>
        {/* Pie Chart */}
        <Col span={12}>
          <Card>
            <Title level={5}>ICU Utilization</Title>

            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={icuData}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={70}
                  outerRadius={100}
                  label={({ name, value }) => `${name}: ${value}`}
                >
                  {icuData.map((entry, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Col>

        /* Bar Chart */
        <Col span={12}>
          <Card>
            <Title level={5}>Alert Distribution</Title>

            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={alertData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />

                <Bar dataKey="critical" fill="#ff4d4f" />
                <Bar dataKey="warning" fill="#faad14" />
                <Bar dataKey="info" fill="#1677ff" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>
    </div>
    
  );
};

export default ReportsPage;