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
  Tag,
} from "antd";
import type { ColumnsType } from "antd/es/table";

import {
  getRoles,
  getPermissions,
  createRole,
  updateRole,
} from "../../api/adminApi";

import type { Role, RolePayload } from "../../types/role";

const { Title } = Typography;

interface RoleFormValues {
  name: string;
  description?: string;
  permissions: string[];
}

const RoleManager: React.FC = () => {
  const [roles, setRoles] = useState<Role[]>([]);
  const [permissions, setPermissions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingRole, setEditingRole] = useState<Role | null>(null);

  const [form] = Form.useForm<RoleFormValues>();

  async function loadData() {
    try {
      setLoading(true);

      const [rolesData, permissionsData] = await Promise.all([
        getRoles(),
        getPermissions(),
      ]);

      setRoles(rolesData);
      setPermissions(permissionsData);
    } catch (error) {
      console.error("Failed to load roles or permissions:", error);
      message.error("Failed to load roles or permissions");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  function openModal(role?: Role) {
    setEditingRole(role || null);

    if (role) {
      form.setFieldsValue({
        name: role.name,
        description: role.description,
        permissions: role.permissions,
      });
    } else {
      form.resetFields();
    }

    setModalVisible(true);
  }

  async function handleOk() {
    try {
      const values = await form.validateFields();

      const payload: RolePayload = {
        name: values.name,
        description: values.description,
        permission_names: values.permissions || [],
      };

      setSubmitting(true);

      if (editingRole) {
        await updateRole(editingRole.id, payload);
        message.success("Role updated");
      } else {
        await createRole(payload);
        message.success("Role created");
      }

      setModalVisible(false);
      setEditingRole(null);
      form.resetFields();
      loadData();
    } catch (error) {
      // AntD form validation handles validation errors
      if (error) {
        console.error("Failed to save role:", error);
      }
    } finally {
      setSubmitting(false);
    }
  }

  const columns: ColumnsType<Role> = [
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
      title: "Description",
      dataIndex: "description",
      key: "description",
      render: (value?: string) => value || "-",
      width: 240,
    },
    {
      title: "Permissions",
      dataIndex: "permissions",
      key: "permissions",
      render: (perms: string[]) =>
        perms?.length ? (
          <>
            {perms.map((perm) => (
              <Tag key={perm}>{perm}</Tag>
            ))}
          </>
        ) : (
          "-"
        ),
      width: 420,
    },
    {
      title: "Actions",
      key: "actions",
      width: 120,
      render: (_: unknown, record: Role) => (
        <Button type="link" onClick={() => openModal(record)}>
          Edit
        </Button>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Title level={3}>Role Management</Title>

      <Button
        type="primary"
        onClick={() => openModal()}
        style={{ marginBottom: 16 }}
      >
        Add Role
      </Button>

      <Table
        rowKey="id"
        columns={columns}
        dataSource={roles}
        loading={loading}
        bordered
        scroll={{ x: 1200 }}
      />

      <Modal
        title={editingRole ? "Edit Role" : "Add Role"}
        open={modalVisible}
        onOk={handleOk}
        onCancel={() => {
          setModalVisible(false);
          setEditingRole(null);
          form.resetFields();
        }}
        confirmLoading={submitting}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="Name"
            rules={[{ required: true, message: "Please enter role name" }]}
          >
            <Input placeholder="e.g. ICU Admin" />
          </Form.Item>

          <Form.Item name="description" label="Description">
            <Input placeholder="Optional role description" />
          </Form.Item>

          <Form.Item name="permissions" label="Permissions">
            <Select
              mode="multiple"
              placeholder="Select permissions"
              options={permissions.map((permission) => ({
                label: permission,
                value: permission,
              }))}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default RoleManager;