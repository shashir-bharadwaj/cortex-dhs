import React, { useEffect, useState } from "react";
import { Table, Button, Modal, Form, Input, message, Typography } from "antd";
import type { ColumnsType } from "antd/es/table";

import {
  getDeviceTypes,
  createDeviceType,
  updateDeviceType,
} from "../../api/adminApi";

import type { DeviceType, DeviceTypePayload } from "../../types/deviceType";

const { Title } = Typography;

const DeviceTypeManager: React.FC = () => {
  const [deviceTypes, setDeviceTypes] = useState<DeviceType[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editing, setEditing] = useState<DeviceType | null>(null);

  const [form] = Form.useForm<DeviceTypePayload>();

  async function loadDeviceTypes() {
    try {
      setLoading(true);
      const data = await getDeviceTypes();
      setDeviceTypes(data);
    } catch (error) {
      console.error("Failed to load device types:", error);
      message.error("Failed to load device types");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDeviceTypes();
  }, []);

  function openModal(record?: DeviceType) {
    setEditing(record || null);

    if (record) {
      form.setFieldsValue({
        name: record.name,
        company: record.company,
        output_spec: record.output_spec,
        adapter_name: record.adapter_name,
      });
    } else {
      form.resetFields();
    }

    setModalVisible(true);
  }

  async function handleOk() {
    try {
      const values = await form.validateFields();

      setSubmitting(true);

      if (editing) {
        await updateDeviceType(editing.id, values);
        message.success("Device type updated");
      } else {
        await createDeviceType(values);
        message.success("Device type created");
      }

      setModalVisible(false);
      form.resetFields();
      setEditing(null);
      loadDeviceTypes();
    } catch (error) {
      // AntD form validation errors are handled automatically
      if (error) {
        console.error("Failed to save device type:", error);
      }
    } finally {
      setSubmitting(false);
    }
  }

  const columns: ColumnsType<DeviceType> = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      width: 80,
    },
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
      width: 180,
    },
    {
      title: "Company",
      dataIndex: "company",
      key: "company",
      width: 180,
    },
    {
      title: "Output",
      dataIndex: "output_spec",
      key: "output_spec",
      render: (value?: string) => value || "-",
      width: 220,
    },
    {
      title: "Adapter",
      dataIndex: "adapter_name",
      key: "adapter_name",
      render: (value?: string) => value || "-",
      width: 180,
    },
    {
      title: "Created",
      dataIndex: "created_at",
      key: "created_at",
      render: (value: string) => new Date(value).toLocaleString(),
      width: 180,
    },
    {
      title: "Actions",
      key: "actions",
      width: 120,
      render: (_: unknown, record: DeviceType) => (
        <Button type="link" onClick={() => openModal(record)}>
          Edit
        </Button>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Title level={3}>Device Type Management</Title>

      <Button
        type="primary"
        onClick={() => openModal()}
        style={{ marginBottom: 16 }}
      >
        Add Device Type
      </Button>

      <Table
        rowKey="id"
        columns={columns}
        dataSource={deviceTypes}
        loading={loading}
        bordered
        scroll={{ x: 1200 }}
      />

      <Modal
        title={editing ? "Edit Device Type" : "Add Device Type"}
        open={modalVisible}
        onOk={handleOk}
        onCancel={() => {
          setModalVisible(false);
          setEditing(null);
          form.resetFields();
        }}
        confirmLoading={submitting}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="Name"
            rules={[{ required: true, message: "Please enter device type name" }]}
          >
            <Input placeholder="e.g. Multiparameter Monitor" />
          </Form.Item>

          <Form.Item
            name="company"
            label="Company"
            rules={[{ required: true, message: "Please enter company name" }]}
          >
            <Input placeholder="e.g. Philips" />
          </Form.Item>

          <Form.Item name="output_spec" label="Output Spec">
            <Input placeholder="e.g. HL7 / JSON / CSV" />
          </Form.Item>

          <Form.Item name="adapter_name" label="Adapter Name">
            <Input placeholder="e.g. philips_hl7_adapter" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default DeviceTypeManager;