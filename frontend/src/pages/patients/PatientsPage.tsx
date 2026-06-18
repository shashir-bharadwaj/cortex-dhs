import React, { useCallback, useEffect, useState } from "react";
import {
  Table,
  Input,
  Button,
  Typography,
  Tag,
  Modal,
  DatePicker,
  Select,
  Popconfirm,
  Tooltip,
  message,
} from "antd";
import type { ColumnsType } from "antd/es/table";
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import dayjs from "dayjs";
import {
  getPatientsPaged,
  createPatient,
  updatePatient,
  deletePatient,
} from "../../api/patientApi";
import { Patient } from "../../types/patient";

const { Title } = Typography;

const BRAND_PURPLE = "#5b2be0";
const PAGE_SIZE = 10;

interface AddForm {
  name: string;
  age: string;
  gender: string | undefined;
  contactNumber: string;
  diagnosis: string;
  admittedDate: dayjs.Dayjs | null;
  doctor: string;
}

const EMPTY_FORM: AddForm = {
  name: "",
  age: "",
  gender: undefined,
  contactNumber: "",
  diagnosis: "",
  admittedDate: null,
  doctor: "",
};

const GENDER_OPTIONS = [
  { value: "MALE", label: "Male" },
  { value: "FEMALE", label: "Female" },
  { value: "OTHER", label: "Other" },
];

const PatientsPage: React.FC = () => {
  const navigate = useNavigate();

  const [patients, setPatients] = useState<Patient[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState("");

  const [modalOpen, setModalOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState<AddForm>(EMPTY_FORM);
  const [saving, setSaving] = useState(false);

  const fetchPage = useCallback(async (targetPage: number) => {
    setLoading(true);
    try {
      const { items, total: count } = await getPatientsPaged({
        limit: PAGE_SIZE,
        offset: (targetPage - 1) * PAGE_SIZE,
      });
      setPatients(items);
      setTotal(count);
      setPage(targetPage);
    } catch (err) {
      console.error("Failed to fetch patients:", err);
      message.error("Failed to load patients");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPage(1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function openAdd() {
    setEditingId(null);
    setForm(EMPTY_FORM);
    setModalOpen(true);
  }

  function openEdit(p: Patient) {
    setEditingId(p.id);
    setForm({
      name: p.name ?? "",
      age: p.age != null ? String(p.age) : "",
      gender: p.gender ? p.gender.toUpperCase() : undefined,
      contactNumber: p.contactNumber ?? "",
      diagnosis: p.diagnosis ?? "",
      admittedDate: p.admissionTime ? dayjs(p.admissionTime) : null,
      doctor: p.doctor ?? "",
    });
    setModalOpen(true);
  }

  async function handleSave() {
    if (!form.name.trim()) {
      message.warning("Name is required");
      return;
    }
    const ageNum = form.age.trim() ? parseInt(form.age, 10) : undefined;
    const payload = {
      name: form.name.trim(),
      age: Number.isNaN(ageNum as number) ? undefined : ageNum,
      gender: form.gender,
      contactNumber: form.contactNumber.trim() || undefined,
      diagnosis: form.diagnosis.trim() || undefined,
      admissionTime: form.admittedDate
        ? form.admittedDate.toISOString()
        : undefined,
      doctor: form.doctor.trim() || undefined,
    };
    try {
      setSaving(true);
      if (editingId != null) {
        await updatePatient(editingId, payload);
        message.success("Patient updated");
      } else {
        await createPatient(payload);
        message.success("Patient added");
      }
      setModalOpen(false);
      setForm(EMPTY_FORM);
      setEditingId(null);
      fetchPage(editingId != null ? page : 1);
    } catch (err) {
      console.error("Save patient failed:", err);
      message.error("Failed to save patient");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id: number) {
    try {
      await deletePatient(id);
      message.success("Patient deleted");
      const newTotal = Math.max(0, total - 1);
      const lastPage = Math.max(1, Math.ceil(newTotal / PAGE_SIZE));
      fetchPage(Math.min(page, lastPage));
    } catch (err) {
      console.error("Delete patient failed:", err);
      message.error("Failed to delete patient");
    }
  }

  const filtered = query.trim()
    ? patients.filter((p) => {
        const q = query.toLowerCase();
        return (
          p.name?.toLowerCase().includes(q) ||
          p.mrn?.toLowerCase().includes(q)
        );
      })
    : patients;

  const columns: ColumnsType<Patient> = [
    {
      title: "MRN-NO",
      dataIndex: "mrn",
      key: "mrn",
      render: (mrn: string, record) => (
        <a
          style={{ color: BRAND_PURPLE, fontWeight: 600 }}
          onClick={() => navigate(`/patients/${record.id}`)}
        >
          {mrn ?? "—"}
        </a>
      ),
    },
    { title: "Name", dataIndex: "name", key: "name" },
    {
      title: "Age/Gender",
      key: "ageGender",
      render: (_, r) =>
        `${r.age ?? "—"}/${r.gender ? r.gender.toUpperCase() : "—"}`,
    },
    {
      title: "Contact Number",
      dataIndex: "contactNumber",
      key: "contactNumber",
      render: (v: string) => v ?? "—",
    },
    {
      title: "Diagnosis",
      dataIndex: "diagnosis",
      key: "diagnosis",
      render: (v: string) => v ?? "—",
    },
    {
      title: "Admitted Date",
      dataIndex: "admissionTime",
      key: "admissionTime",
      render: (t: string) =>
        t ? dayjs(t).format("YYYY-MM-DD HH:mm") : "—",
    },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (s: string) => (
        <Tag color={s === "admitted" ? "green" : "default"}>{s}</Tag>
      ),
    },
    {
      title: "Action",
      key: "action",
      width: 96,
      render: (_, record) => (
        <div style={{ display: "flex", gap: 12 }}>
          <Tooltip title="Edit">
            <EditOutlined
              style={{ color: BRAND_PURPLE, cursor: "pointer" }}
              onClick={() => openEdit(record)}
            />
          </Tooltip>
          <Popconfirm
            title="Delete this patient?"
            description="This permanently removes the patient and their records."
            okText="Delete"
            okButtonProps={{ danger: true }}
            onConfirm={() => handleDelete(record.id)}
          >
            <Tooltip title="Delete">
              <DeleteOutlined style={{ color: "#ff4d4f", cursor: "pointer" }} />
            </Tooltip>
          </Popconfirm>
        </div>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginBottom: 16,
          gap: 12,
          flexWrap: "wrap",
        }}
      >
        <Title level={3} style={{ margin: 0 }}>
          Patients
        </Title>
        <div style={{ display: "flex", gap: 12 }}>
          <Input
            allowClear
            placeholder="Filter by name or MRN…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ width: 260, borderRadius: 8 }}
          />
          <Button
            type="primary"
            icon={<PlusOutlined />}
            style={{ background: BRAND_PURPLE, borderColor: BRAND_PURPLE }}
            onClick={openAdd}
          >
            Add Patient
          </Button>
        </div>
      </div>

      <Table<Patient>
        dataSource={filtered}
        columns={columns}
        rowKey="id"
        loading={loading}
        style={{ background: "#fff", borderRadius: 10 }}
        pagination={{
          current: page,
          pageSize: PAGE_SIZE,
          total,
          showSizeChanger: false,
          onChange: (p) => fetchPage(p),
        }}
      />

      {/* Add / Edit modal */}
      <Modal
        title={editingId != null ? "Edit Patient" : "Add Patient"}
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        onOk={handleSave}
        confirmLoading={saving}
        okText="Save"
        width={460}
        okButtonProps={{
          size: "large",
          style: { background: BRAND_PURPLE, borderColor: BRAND_PURPLE },
        }}
        cancelButtonProps={{ size: "large" }}
        destroyOnClose
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 14,
            marginTop: 12,
          }}
        >
          <Input
            size="large"
            placeholder="Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
          <Input
            size="large"
            type="number"
            placeholder="Age"
            value={form.age}
            onChange={(e) => setForm({ ...form, age: e.target.value })}
          />
          <Select
            size="large"
            placeholder="Gender"
            value={form.gender}
            onChange={(v) => setForm({ ...form, gender: v })}
            options={GENDER_OPTIONS}
            style={{ width: "100%" }}
          />
          <Input
            size="large"
            placeholder="Contact Number"
            value={form.contactNumber}
            onChange={(e) =>
              setForm({ ...form, contactNumber: e.target.value })
            }
          />
          <Input
            size="large"
            placeholder="Diagnosis"
            value={form.diagnosis}
            onChange={(e) => setForm({ ...form, diagnosis: e.target.value })}
          />
          <div>
            <Typography.Text style={{ fontSize: 13, color: "#555" }}>
              Admitted Date
            </Typography.Text>
            <DatePicker
              size="large"
              style={{ width: "100%", marginTop: 4 }}
              value={form.admittedDate}
              onChange={(d) => setForm({ ...form, admittedDate: d })}
              format="DD-MM-YYYY"
              placeholder="dd-mm-yyyy"
            />
          </div>
          <Input
            size="large"
            placeholder="Doctor"
            value={form.doctor}
            onChange={(e) => setForm({ ...form, doctor: e.target.value })}
          />
        </div>
      </Modal>
    </div>
  );
};

export default PatientsPage;
