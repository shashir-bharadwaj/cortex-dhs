import React, { useEffect, useState } from "react";
import {
  Table,
  Button,
  Modal,
  Form,
  Input,
  Select,
  message,
  Typography,
} from "antd";
import type { ColumnsType } from "antd/es/table";

import { getUsers, createUser } from "../../api/userApi";
import { getRoles } from "../../api/adminApi";

import type { User, CreateUserPayload, RoleOption } from "../../types/user";
import type { Role } from "../../types/role";

const { Title } = Typography;

const UserManager: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [roles, setRoles] = useState<RoleOption[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);

  const [form] = Form.useForm<CreateUserPayload>();

  async function loadData() {
    try {
      setLoading(true);

      const [usersData, rolesData] = await Promise.all([
        getUsers(),
        getRoles(),
      ]);

      setUsers(usersData);
      setRoles(
        rolesData.map((role: Role) => ({
          id: role.id,
          name: role.name,
        }))
      );
    } catch (error) {
      console.error("Failed to load users or roles:", error);
      message.error("Failed to load users or roles");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  function openModal() {
    form.resetFields();
    setModalVisible(true);
  }

  async function handleOk() {
    try {
      const values = await form.validateFields();

      setSubmitting(true);
      await createUser(values);

      message.success("User created");
      setModalVisible(false);
      form.resetFields();
      loadData();
    } catch (error) {
      // AntD validation errors are handled automatically
      if (error) {
        console.error("Failed to create user:", error);
      }
    } finally {
      setSubmitting(false);
    }
  }

  const columns: ColumnsType<User> = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      width: 80,
    },
    {
      title: "Username",
      dataIndex: "username",
      key: "username",
      width: 180,
    },
    {
      title: "Full Name",
      dataIndex: "full_name",
      key: "full_name",
      width: 220,
    },
    {
      title: "Email",
      dataIndex: "email",
      key: "email",
      width: 240,
    },
    {
      title: "Role ID",
      dataIndex: "role_id",
      key: "role_id",
      width: 100,
    },
    {
      title: "Role",
      dataIndex: "role",
      key: "role",
      render: (value?: string) => value || "-",
      width: 160,
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Title level={3}>User Management</Title>

      <Button
        type="primary"
        onClick={openModal}
        style={{ marginBottom: 16 }}
      >
        Add User
      </Button>

      <Table
        rowKey="id"
        columns={columns}
        dataSource={users}
        loading={loading}
        bordered
        scroll={{ x: 1100 }}
      />

      <Modal
        title="Add User"
        open={modalVisible}
        onOk={handleOk}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        confirmLoading={submitting}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="username"
            label="Username"
            rules={[{ required: true, message: "Please enter username" }]}
          >
            <Input placeholder="e.g. John" />
          </Form.Item>

          <Form.Item
            name="full_name"
            label="Full Name"
            rules={[{ required: true, message: "Please enter full name" }]}
          >
            <Input placeholder="e.g. John Doe" />
          </Form.Item>

          <Form.Item
            name="email"
            label="Email"
            rules={[
              { required: true, message: "Please enter email" },
              { type: "email", message: "Please enter a valid email" },
            ]}
          >
            <Input placeholder="e.g. xyz@example.com" />
          </Form.Item>

          <Form.Item
            name="password"
            label="Password"
            rules={[{ required: true, message: "Please enter password" }]}
          >
            <Input.Password placeholder="Enter password" />
          </Form.Item>

          <Form.Item
            name="role_id"
            label="Role"
            rules={[{ required: true, message: "Please select a role" }]}
          >
            <Select
              placeholder="Select a role"
              options={roles.map((role) => ({
                label: role.name,
                value: role.id,
              }))}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default UserManager;