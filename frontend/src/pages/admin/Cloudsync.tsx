import React, { useEffect, useState } from "react";
import { Card, Row, Col, Table, Tag, Typography, Button } from "antd";
import {
  ClockCircleOutlined,
  DatabaseOutlined,
  WarningOutlined,
  CloudOutlined,
} from "@ant-design/icons";
import { getCloudSyncStatus, CloudSyncResponse, HospitalSync, CloudSummary } from "../../api/adminApi";

const { Title, Text } = Typography;


const getStatusTag = (status: string) => {
  return status === "Connected" ? (
    <Tag color="green">● Connected</Tag>
  ) : (
    <Tag color="orange">● Delayed</Tag>
  );
};

/* ================= COMPONENT ================= */

const CloudSyncPage = () => {
  const [summary, setSummary] = useState<CloudSummary>({ lastSync: "-", dataSent: "-", errors: 0, hospitals: 0 });
  const [hospitalData, setHospitalData] = useState<HospitalSync[]>([]);

  useEffect(() => {
    let mounted = true;
    getCloudSyncStatus()
      .then((res: CloudSyncResponse) => {
        if (!mounted) return;
        setSummary(res.summary);
        setHospitalData(res.hospitals);
      })
      .catch(() => {
        // keep defaults on error
      });
    return () => {
      mounted = false;
    };
  }, []);

  const columns = [
    {
      title: "Hospital",
      dataIndex: "name",
      render: (text: string) => <b>{text}</b>,
    },
    {
      title: "City",
      dataIndex: "city",
    },
    {
      title: "Sync Status",
      dataIndex: "status",
      render: (status: string) => getStatusTag(status),
    },
    {
      title: "Last Sync",
      dataIndex: "lastSync",
    },
   
  ];

  return (
    <div style={{ padding: 24 }}>
      <div style={{ marginBottom: 20 }}>
        <Title level={3}>Cloud Sync Monitoring</Title>
        <Text type="secondary">
          Hospital to cloud data synchronization status
        </Text>
      </div>

      <Row gutter={16} style={{ marginBottom: 20 }}>
        <Col span={6}>
          <Card>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <div>
                <Text type="secondary">LAST SYNC</Text>
                <Title level={4}>{summary.lastSync}</Title>
              </div>
              <ClockCircleOutlined style={{ fontSize: 24 }} />
            </div>
          </Card>
        </Col>

        <Col span={6}>
          <Card style={{ background: "#1f9d9d", color: "#fff" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <div>
                <Text style={{ color: "#fff" }}>DATA SENT</Text>
                <Title level={4} style={{ color: "#fff" }}>
                  {summary.dataSent}
                </Title>
              </div>
              <DatabaseOutlined style={{ fontSize: 24 }} />
            </div>
          </Card>
        </Col>

        <Col span={6}>
          <Card style={{ background: "#fa8c16", color: "#fff" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <div>
                <Text style={{ color: "#fff" }}>SYNC ERRORS</Text>
                <Title level={4} style={{ color: "#fff" }}>
                  {summary.errors}
                </Title>
              </div>
              <WarningOutlined style={{ fontSize: 24 }} />
            </div>
          </Card>
        </Col>

        <Col span={6}>
          <Card style={{ background: "#52c41a", color: "#fff" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <div>
                <Text style={{ color: "#fff" }}>HOSPITALS</Text>
                <Title level={4} style={{ color: "#fff" }}>
                  {summary.hospitals}
                </Title>
              </div>
              <CloudOutlined style={{ fontSize: 24 }} />
            </div>
          </Card>
        </Col>
      </Row>
      <div style={{ marginBottom: 12 }}>
        <Button type="primary" onClick={() => { getCloudSyncStatus().then(res => { setSummary(res.summary); setHospitalData(res.hospitals); }).catch(()=>{}); }}>
          Refresh
        </Button>
      </div>

      <Card>
        <Table
          columns={columns}
          dataSource={hospitalData}
          rowKey="id"
          pagination={false}
        />
      </Card>
    </div>
  );
};

export default CloudSyncPage;