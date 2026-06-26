import React, { useEffect, useState } from "react";

import { Tag, Typography, Button, Tabs, Checkbox, Collapse, Modal, Row, Col } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { Pencil, Trash2 } from "lucide-react";
import CommonTable from "../shared/table";
import DeleteConfirmPopup from "../icu/DeleteConfirmationPopup";
import {
  addUser,
  createRolePermission,
  getRolePermission,
  getUsers,
  updateRolePermission,
  updateUser,
} from "../../Service/adminService";

const { Title, Text } = Typography;
const { Panel } = Collapse;

interface UserData {
  userId: number;
  firstName: string;
  lastName: string;
  role: string;
  email: string;
  isActive: string;
  department: string;
  assignedIcu: string;
}

interface RolePermission {
  module: string;
  moduleName: string;
  allowedActions: string[];
}

interface Role {
  roleId: number;
  role: string;
  description?: string;
  permissions: RolePermission[];
}

type PermissionModule = "alarms" | "bed_management" | "device_management" | "hospitals";
type PermissionAction = "view" | "create" | "modify" | "delete";

type PermissionState = {
  [key in PermissionModule]: {
    [action in PermissionAction]: boolean;
  };
};

const permissionsData: { key: PermissionModule; title: string }[] = [
  { key: "alarms", title: "Alarms" },
  { key: "bed_management", title: "Bed Management" },
  { key: "device_management", title: "Device Management" },
  { key: "hospitals", title: "Hospitals" },
];

const initialPermissions: PermissionState = {
  alarms: { view: false, create: false, modify: false, delete: false },
  bed_management: { view: false, create: false, modify: false, delete: false },
  device_management: { view: false, create: false, modify: false, delete: false },
  hospitals: { view: false, create: false, modify: false, delete: false },
};

const initialForm = {
  userId: 0,
  firstName: "",
  lastName: "",
  role: "",
  email: "",
  isActive: "",
  department: "",
  assignedIcu: "",
};

const getRoleTag = (role: string) => {
  const colors: Record<string, string> = {
    ADMIN: "green",
    DOCTOR: "blue",
    NURSE: "purple",
  };

  return <Tag color={colors[role] || "default"}>{role}</Tag>;
};

const UsersAndRolesPage = () => {
  const [activeTab, setActiveTab] = useState("users");
  const [openRoleModal, setOpenRoleModal] = useState(false);
  const [openUserModal, setOpenUserModal] = useState(false);
  const [userdata, setData] = useState<UserData[]>([]);
  const [roledata, setRole] = useState<Role[]>([]);
  const [isEdit, setIsEdit] = useState(false);
  const [isRoleEdit, setIsRoleEdit] = useState(false);
  const [form, setForm] = useState(initialForm);
  const [roleName, setRoleName] = useState("");
  const [roleDescription, setRoleDescription] = useState("");
  const [permissions, setPermissions] = useState<PermissionState>(initialPermissions);
  const [selectedRoleId, setSelectedRoleId] = useState<number>(0);
  const [openDelete, setOpenDelete] = useState(false);
  const [selectedDeleteId, setSelectedDeleteId] = useState<number | null>(null);

  useEffect(() => {
    loadUsers();
    loadRoles();
  }, []);

  const loadUsers = async () => {
    try {
      const response = await getUsers();
      setData(response);
    } catch (error) {
      console.error("Something went wrong. Please try again.", error);
    }
  };

  const loadRoles = async () => {
    try {
      const response = await getRolePermission();
      setRole(response.rolePermissions);
    } catch (error) {
      console.error("Something went wrong. Please try again.", error);
    }
  };

  const userColumns = [
    { title: "Name", dataIndex: "firstName", render: (text: string) => <b>{text}</b> },
    { title: "Role", dataIndex: "role", render: (role: string) => getRoleTag(role) },
    { title: "Department", dataIndex: "department" },
    { title: "Assigned ICU", dataIndex: "assignedIcu" },
    { title: "Email", dataIndex: "email" },
    { title: "Status", dataIndex: "isActive" },
  ];

  const roleColumns = [
    { title: "Role Name", dataIndex: "role", key: "role" },
    { title: "Description", dataIndex: "description", key: "description" },
  ];

  const handleEdit = (row: UserData) => {
    setIsEdit(true);
    setForm({
      userId: row.userId,
      firstName: row.firstName,
      lastName: row.lastName,
      role: row.role,
      email: row.email,
      isActive: row.isActive,
      department: row.department,
      assignedIcu: row.assignedIcu,
    });
    setOpenUserModal(true);
  };

  const handleRoleEdit = (row: Role) => {
    setSelectedRoleId(row.roleId);
    setIsRoleEdit(true);
    setRoleName(row.role);
    setRoleDescription(row.description || "");

    const formattedPermissions: PermissionState = { ...initialPermissions };
    row.permissions.forEach((permissionItem) => {
      const moduleKey = permissionItem.module.toLowerCase() as PermissionModule;
      formattedPermissions[moduleKey] = {
        view: permissionItem.allowedActions.includes("VIEW"),
        create: permissionItem.allowedActions.includes("CREATE"),
        modify: permissionItem.allowedActions.includes("MODIFY"),
        delete: permissionItem.allowedActions.includes("DELETE"),
      };
    });

    setPermissions(formattedPermissions);
    setOpenRoleModal(true);
  };

  const handleAddUser = () => {
    setIsEdit(false);
    setForm(initialForm);
    setOpenUserModal(true);
  };

  const handleAddRole = () => {
    setOpenRoleModal(true);
    setIsRoleEdit(false);
    setRoleName("");
    setRoleDescription("");
    setPermissions(initialPermissions);
  };

  const handleSubmit = async () => {
    try {
      if (isEdit) {
        const response = await updateUser(form.userId, form);
        setData((prev) => prev.map((item) => (item.userId === form.userId ? response : item)));
      } else {
        const response = await addUser(form);
        setData((prev) => [...prev, response]);
      }
      setOpenUserModal(false);
    } catch (error) {
      console.error("Failed to update", error);
    }
  };

  const handleCheckboxChange = (section: PermissionModule, permission: PermissionAction, checked: boolean) => {
    setPermissions((prev) => ({
      ...prev,
      [section]: {
        ...prev[section],
        [permission]: checked,
      },
    }));
  };

  const AddRole = async () => {
    const payload = {
      name: roleName,
      description: roleDescription,
      permissions: Object.entries(permissions).map(([module, actions]) => ({
        module: module.toUpperCase(),
        allowedActions: Object.entries(actions)
          .filter(([, value]) => value)
          .map(([key]) => key.toUpperCase()),
      })),
    };

    try {
      if (isRoleEdit) {
        const response = await updateRolePermission(selectedRoleId, payload);
        setRole((prev) => prev.map((item) => (item.roleId === selectedRoleId ? response : item)));
      } else {
        const response = await createRolePermission(payload);
        setRole((prev) => [...prev, response]);
      }
      await loadRoles();
      setOpenRoleModal(false);
      setRoleName("");
      setRoleDescription("");
      setPermissions(initialPermissions);
    } catch (error) {
      console.error("Failed to save role", error);
    }
  };

  const styles = {
    page: { padding: 24 },
    headerRow: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 },
    title: { margin: 0 },
    subtitle: { color: "#6b7280", fontSize: 14, marginTop: 4 },
    button: { backgroundColor: "#2563eb", color: "#ffffff", border: "none" },
    actionRow: { display: "flex", gap: "0.75rem", alignItems: "center" },
    actionIcon: { cursor: "pointer" },
    modalContent: { padding: 16 },
    input: {
      width: "100%",
      border: "1px solid #d1d5db",
      padding: "0.5rem",
      borderRadius: 6,
      marginBottom: 12,
      boxSizing: "border-box" as const,
    },
    row: { display: "flex", gap: 16, marginBottom: 16 },
    modalButtonRow: { display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 24 },
    gridTwo: { display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 16 },
  };

  return (
    <div style={styles.page}>
      <div style={styles.headerRow}>
        <div>
          <Title level={3} style={styles.title}>
            Users & Roles
          </Title>
          <Text type="secondary" style={styles.subtitle}>
            Manage hospital users and role-based access
          </Text>
        </div>

        <Button type="primary" icon={<PlusOutlined />} onClick={() => (activeTab === "users" ? handleAddUser() : handleAddRole())} style={styles.button}>
          {activeTab === "users" ? "Create User" : "Create Role"}
        </Button>
      </div>

      <Tabs activeKey={activeTab} onChange={setActiveTab} items={[{ key: "users", label: "User Management" }, { key: "roles", label: "Role Permissions" }]} />

      {activeTab === "users" && (
        <CommonTable
          columns={userColumns}
          data={userdata}
          renderActions={(row: Record<string, any>) => (
            <div style={styles.actionRow}>
              <Pencil size={18} onClick={() => handleEdit(row as UserData)} style={{ ...styles.actionIcon, color: "#2563eb" }} />
              <Trash2 size={18} onClick={() => { setSelectedDeleteId(row.userId); setOpenDelete(true); }} style={{ ...styles.actionIcon, color: "#dc2626" }} />
            </div>
          )}
        />
      )}

      {activeTab === "roles" && (
        <CommonTable
          columns={roleColumns}
          data={roledata}
          renderActions={(row: Record<string, any>) => (
            <div style={styles.actionRow}>
              <Pencil size={18} onClick={() => handleRoleEdit(row as Role)} style={{ ...styles.actionIcon, color: "#2563eb" }} />
              <Trash2 size={18} onClick={() => { setSelectedDeleteId(row.roleId); setOpenDelete(true); }} style={{ ...styles.actionIcon, color: "#dc2626" }} />
            </div>
          )}
        />
      )}

      <DeleteConfirmPopup
        open={openDelete}
        id={selectedDeleteId ?? 0}
        module="users"
        message="Are you sure you want to delete this item?"
        onClose={() => setOpenDelete(false)}
        onSuccess={() => {
          setOpenDelete(false);
          if (activeTab === "users") loadUsers(); else loadRoles();
        }}
      />

      <Modal title={isRoleEdit ? "Edit Role Permission" : "Create Role Permission"} open={openRoleModal} onCancel={() => setOpenRoleModal(false)} footer={null} width={600}>
        <div style={styles.modalContent}>
          <Row gutter={16} style={{ marginBottom: 16 }}>
            <Col span={24}>
              <input type="text" placeholder="Role Name" style={styles.input} value={roleName} onChange={(e) => setRoleName(e.target.value)} />
            </Col>
          </Row>

          <Row gutter={16} style={{ marginBottom: 16 }}>
            <Col span={24}>
              <input type="text" placeholder="Role Description" style={styles.input} value={roleDescription} onChange={(e) => setRoleDescription(e.target.value)} />
            </Col>
          </Row>

          <Collapse defaultActiveKey={["0"]}>
            {permissionsData.map((item, index) => (
              <Panel header={item.title} key={index}>
                <div style={styles.gridTwo}>
                  {(["view", "create", "modify", "delete"] as PermissionAction[]).map((permission) => (
                    <Checkbox key={permission} checked={permissions[item.key][permission]} onChange={(e) => handleCheckboxChange(item.key, permission, e.target.checked)}>
                      {permission.charAt(0).toUpperCase() + permission.slice(1)}
                    </Checkbox>
                  ))}
                </div>
              </Panel>
            ))}
          </Collapse>

          <div style={styles.modalButtonRow}>
            <Button onClick={() => setOpenRoleModal(false)}>Cancel</Button>
            <Button type="primary" onClick={AddRole}>
              {isRoleEdit ? "Update" : "Create"}
            </Button>
          </div>
        </div>
      </Modal>

      <Modal title={isEdit ? "Update User" : "Create User"} open={openUserModal} onCancel={() => setOpenUserModal(false)} footer={null} width={600}>
        <div style={{ padding: 16 }}>
          <div style={styles.gridTwo}>
            <input type="text" placeholder="First Name" style={styles.input} value={form.firstName} onChange={(e) => setForm({ ...form, firstName: e.target.value })} />
            <input type="text" placeholder="Last Name" style={styles.input} value={form.lastName} onChange={(e) => setForm({ ...form, lastName: e.target.value })} />
            <input type="text" placeholder="Email" style={styles.input} value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            <input type="text" placeholder="User Role" style={styles.input} value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} />
            <input type="text" placeholder="Department" style={styles.input} value={form.department} onChange={(e) => setForm({ ...form, department: e.target.value })} />
            <input type="text" placeholder="Assigned ICU" style={styles.input} value={form.assignedIcu} onChange={(e) => setForm({ ...form, assignedIcu: e.target.value })} />
          </div>

          <div style={styles.modalButtonRow}>
            <Button onClick={() => setOpenUserModal(false)}>Cancel</Button>
            <Button type="primary" onClick={handleSubmit}>
              {isEdit ? "Update User" : "Create User"}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default UsersAndRolesPage;
