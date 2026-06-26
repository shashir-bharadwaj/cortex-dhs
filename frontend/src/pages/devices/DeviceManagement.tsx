import React, { useEffect, useState } from "react";
import { Pencil, Trash2 } from "lucide-react";
import CommonTable from "../shared/table";
import DeleteConfirmPopup from "../icu/DeleteConfirmationPopup";
import { addDevice, getDevices, updateDevice } from "../../Service/adminService";

interface DeviceData {
  id: number;
  device_type: string;
  manufacturer: string;
  model: string;
  serial: string;
  bed: string;
  status: string;
}

const DeviceManagement = () => {
  const [open, setOpen] = useState(false);
  const [isEdit, setIsEdit] = useState(false);
  const [selectedId, setSelectedId] = useState<number>(0);
  const [data, setData] = useState<DeviceData[]>([]);
  const [openDelete, setOpenDelete] = useState(false);

  const [form, setForm] = useState<DeviceData>({
    id: 0,
    device_type: "",
    manufacturer: "",
    model: "",
    serial: "",
    bed: "",
    status: "",
  });

  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    try {
      const response = await getDevices();
      setData(response);
    } catch (error) {
      console.error("Something went wrong. Please try again.", error);
    }
  };

  const resetForm = () => {
    setForm({
      id: 0,
      device_type: "",
      manufacturer: "",
      model: "",
      serial: "",
      bed: "",
      status: "",
    });
  };

  const handleEdit = (row: DeviceData) => {
    setIsEdit(true);

    setForm({
      id: row.id,
      device_type: row.device_type,
      manufacturer: row.manufacturer,
      model: row.model,
      serial: row.serial,
      bed: row.bed,
      status: row.status,
    });

    setOpen(true);
  };

  const handleAdd = () => {
    setIsEdit(false);
    resetForm();
    setOpen(true);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async () => {
    try {
      if (isEdit) {
        const response = await updateDevice(form.id, form);
        setData((prev) => prev.map((item) => (item.id === form.id ? response : item)));
      } else {
        const response = await addDevice(form);
        setData((prev) => [...prev, response]);
      }

      setOpen(false);
      resetForm();
    } catch (error) {
      console.error("Failed to upload", error);
    }
  };

  const handleDeleteClick = (id: number) => {
    setSelectedId(id);
    setOpenDelete(true);
  };

  const columns = [
    { title: "DEVICE ID", dataIndex: "id", key: "id" },
    { title: "TYPE", dataIndex: "device_type", key: "device_type" },
    { title: "MANUFACTURER", dataIndex: "manufacturer", key: "manufacturer" },
    { title: "MODEL", dataIndex: "model", key: "model" },
    { title: "SERIAL", dataIndex: "serial", key: "serial" },
    { title: "BED", dataIndex: "bed", key: "bed" },
    { title: "STATUS", dataIndex: "status", key: "status" },
  ];

  const styles = {
    page: {
      padding: "1.5rem",
      backgroundColor: "#f3f4f6",
      minHeight: "100vh",
    },
    headerRow: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      marginBottom: "1rem",
    },
    title: {
      fontSize: "1.25rem",
      fontWeight: 600,
      margin: 0,
    },
    subtitle: {
      color: "#6b7280",
      fontSize: "0.875rem",
      marginTop: "0.25rem",
    },
    addButton: {
      backgroundColor: "#2563eb",
      color: "#ffffff",
      padding: "0.5rem 1rem",
      borderRadius: "0.25rem",
      border: "none",
      cursor: "pointer",
    },
    actionIcon: {
      cursor: "pointer",
    },
    modalOverlay: {
      position: "fixed" as const,
      inset: 0,
      backgroundColor: "rgba(0, 0, 0, 0.4)",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      zIndex: 50,
    },
    modalCard: {
      backgroundColor: "#ffffff",
      padding: "1.5rem",
      borderRadius: "0.25rem",
      width: "24rem",
      maxWidth: "90vw",
    },
    modalTitle: {
      fontSize: "1.125rem",
      fontWeight: 700,
      marginBottom: "1rem",
    },
    input: {
      width: "100%",
      border: "1px solid #d1d5db",
      padding: "0.5rem",
      borderRadius: "0.25rem",
      marginBottom: "0.75rem",
      boxSizing: "border-box" as const,
    },
    buttonRow: {
      display: "flex",
      justifyContent: "flex-end",
      gap: "0.5rem",
    },
    secondaryButton: {
      padding: "0.5rem 1rem",
      border: "1px solid #d1d5db",
      borderRadius: "0.25rem",
      backgroundColor: "#ffffff",
      cursor: "pointer",
    },
    primaryButton: {
      padding: "0.5rem 1rem",
      borderRadius: "0.25rem",
      backgroundColor: "#2563eb",
      color: "#ffffff",
      border: "none",
      cursor: "pointer",
    },
  };

  return (
    <div style={styles.page}>
      <div style={styles.headerRow}>
        <div>
          <h2 style={styles.title}>Device Management</h2>
          <p style={styles.subtitle}>Register and monitor connected medical devices</p>
        </div>

        <button onClick={handleAdd} style={styles.addButton}>
          + Register Device
        </button>
      </div>

      <CommonTable
        columns={columns}
        data={data}
        renderActions={(row: Record<string, any>) => (
          <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
            <Pencil
              size={18}
              onClick={() => handleEdit(row as DeviceData)}
              style={{ ...styles.actionIcon, color: "#2563eb" }}
            />

            <Trash2
              size={18}
              onClick={() => handleDeleteClick(row.id)}
              style={{ ...styles.actionIcon, color: "#dc2626" }}
            />
          </div>
        )}
      />

      <DeleteConfirmPopup
        open={openDelete}
        id={selectedId}
        module="devices"
        message="Are you sure you want to delete this Device?"
        onClose={() => setOpenDelete(false)}
        onSuccess={loadDevices}
      />

      {open && (
        <div style={styles.modalOverlay}>
          <div style={styles.modalCard}>
            <h2 style={styles.modalTitle}>{isEdit ? "Edit Device" : "Register Device"}</h2>

            <input
              type="text"
              name="device_type"
              placeholder="Device Type"
              style={styles.input}
              value={form.device_type}
              onChange={handleChange}
            />

            <input
              type="text"
              name="manufacturer"
              placeholder="Manufacturer"
              style={styles.input}
              value={form.manufacturer}
              onChange={handleChange}
            />

            <input
              type="text"
              name="model"
              placeholder="Model"
              style={styles.input}
              value={form.model}
              onChange={handleChange}
            />

            <input
              type="text"
              name="serial"
              placeholder="Serial"
              style={styles.input}
              value={form.serial}
              onChange={handleChange}
            />

            <input
              type="text"
              name="bed"
              placeholder="Bed"
              style={styles.input}
              value={form.bed}
              onChange={handleChange}
            />

            <input
              type="text"
              name="status"
              placeholder="Status"
              style={styles.input}
              value={form.status}
              onChange={handleChange}
            />

            <div style={styles.buttonRow}>
              <button onClick={() => setOpen(false)} style={styles.secondaryButton}>
                Cancel
              </button>

              <button onClick={handleSubmit} style={styles.primaryButton}>
                {isEdit ? "Update" : "Add"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DeviceManagement;
