import React, { useEffect, useState } from "react";
import { Pencil, Trash2 } from "lucide-react";
import { addBed, getBeds, updateBed } from "../../Service/adminService";
import CommonTable from "../shared/commontable";
import DeleteConfirmPopup from "../icu/DeleteConfirmationPopup";


const BedManagement = () => {
  const initialForm = {
    id: 0,
    bed_id: "",
    bed_type: "",
    department: "",
    ward: "",
    floor: "",
    room: "",
    cleaning_status: "",
    maintenance_status: "",
    operational_status: "",
    last_sanitized: "",
  };

  const [open, setOpen] = useState(false);
  const [isEdit, setIsEdit] = useState(false);
  const [selectedId, setSelectedId] = useState<number>(0);
  const [openDelete, setOpenDelete] = useState(false);


  const [form, setForm] = useState(initialForm);

  interface BedData {
    id: number;
    bed_id: string;
    bed_type: string;
    department: string;
    ward: string;
    floor: string;
    room: string;
    cleaning_status: string;
    maintenance_status: string;
    operational_status: string;
    last_sanitized: string;
  }

  const [data, setData] = useState<BedData[]>([]);

  useEffect(() => {
    loadBeds();
  }, []);

  const loadBeds = async () => {
    try {
      const response = await getBeds();
      setData(response);
    } catch (error) {
      console.error("Error fetching bed data:", error);
    }
  };

  const resetForm = () => {
    setForm(initialForm);
    setIsEdit(false);
  };

  const handleSubmit = async () => {
    try {
      if (isEdit) {
        const response = await updateBed(form.id, form);
        setData((prev) => prev.map((item) => (item.id === form.id ? response : item)));
      } else {
        const response = await addBed(form);
        setData((prev) => [...prev, response]);
      }

      setOpen(false);
      resetForm();
    } catch (error) {
    }
  };

  const columns = [
    { title: "Bed ID", dataIndex: "bed_id", key: "bed_id" },
    { title: "Bed Type", dataIndex: "bed_type", key: "bed_type" },
    { title: "Department", dataIndex: "department", key: "department" },
    { title: "Ward", dataIndex: "ward", key: "ward" },
    { title: "Floor", dataIndex: "floor", key: "floor" },
    { title: "Room", dataIndex: "room", key: "room" },
    { title: "Cleaning Status", dataIndex: "cleaning_status", key: "cleaning_status" },
    { title: "Maintenance Status", dataIndex: "maintenance_status", key: "maintenance_status" },
    { title: "Operational Status", dataIndex: "operational_status", key: "operational_status" },
    {
      title: "Last Sanitized",
      dataIndex: "last_sanitized",
      key: "last_sanitized",
      render: (value: string) => (value ? value.split("T")[0] : ""),
    },
  ];

  const handleEdit = (row: BedData) => {
    setIsEdit(true);

    setForm({
      id: row.id,
      bed_id: row.bed_id || "",
      bed_type: row.bed_type || "",
      department: row.department || "",
      ward: row.ward || "",
      floor: row.floor || "",
      room: row.room || "",
      cleaning_status: row.cleaning_status || "",
      maintenance_status: row.maintenance_status || "",
      operational_status: row.operational_status || "",
      last_sanitized: row.last_sanitized ? row.last_sanitized.split("T")[0] : "",
    });

    setOpen(true);
  };

  const handleAdd = () => {
    resetForm();
    setOpen(true);
  };

  const handleDeleteClick = (id: number) => {
    setSelectedId(id);
    setOpenDelete(true);
  };

  const styles = {
    page: {
      padding: "2rem",
      backgroundColor: "#f3f4f6",
      minHeight: "100vh",
    },
    headerRow: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      marginBottom: "1.5rem",
    },
    title: {
      fontSize: "1.5rem",
      fontWeight: 700,
      margin: 0,
    },
    subtitle: {
      color: "#6b7280",
      fontSize: "0.875rem",
      marginTop: "0.25rem",
    },
    addButton: {
      display: "flex",
      alignItems: "center",
      gap: "0.5rem",
      padding: "0.75rem 1rem",
      borderRadius: "0.375rem",
      backgroundColor: "#2563eb",
      color: "#ffffff",
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
      borderRadius: "0.5rem",
      width: "500px",
      maxWidth: "90vw",
    },
    modalTitle: {
      fontSize: "1.125rem",
      fontWeight: 700,
      marginBottom: "1rem",
    },
    formGrid: {
      display: "grid",
      gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
      gap: "1rem",
      fontSize: "0.875rem",
    },
    input: {
      width: "100%",
      border: "1px solid #d1d5db",
      padding: "0.5rem",
      borderRadius: "0.25rem",
      boxSizing: "border-box" as const,
      marginBottom: "0.75rem",
    },
    buttonRow: {
      display: "flex",
      justifyContent: "flex-end",
      gap: "0.5rem",
      marginTop: "1rem",
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
            <h1 style={styles.title}>Bed Management</h1>
            <p style={styles.subtitle}>Configure and monitor ICU beds</p>
          </div>

          <button style={styles.addButton} onClick={handleAdd}>
            Add Bed
          </button>
        </div>

        <CommonTable
          columns={columns}
          data={data}
          renderActions={(row: BedData) => (
            <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
              <Pencil
                size={18}
                onClick={() => handleEdit(row)}
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
          module="beds"
          message="Are you sure you want to delete this Bed?"
          onClose={() => setOpenDelete(false)}
          onSuccess={loadBeds}
        />

        {open && (
          <div style={styles.modalOverlay}>
            <div style={styles.modalCard}>
              <h2 style={styles.modalTitle}>{isEdit ? "Update Bed" : "Add Bed"}</h2>

              <div style={styles.formGrid}>
                <input
                  type="text"
                  placeholder="Bed Id"
                  style={styles.input}
                  value={form.bed_id}
                  onChange={(e) => setForm({ ...form, bed_id: e.target.value })}
                />

                <input
                  type="text"
                  placeholder="Bed Type"
                  style={styles.input}
                  value={form.bed_type}
                  onChange={(e) => setForm({ ...form, bed_type: e.target.value })}
                />
              </div>

              <div style={styles.formGrid}>
                <input
                  type="text"
                  placeholder="ICU / Ward"
                  style={styles.input}
                  value={form.ward}
                  onChange={(e) => setForm({ ...form, ward: e.target.value })}
                />

                <input
                  type="text"
                  placeholder="Department"
                  style={styles.input}
                  value={form.department}
                  onChange={(e) => setForm({ ...form, department: e.target.value })}
                />
              </div>

              <div style={styles.formGrid}>
                <input
                  type="text"
                  placeholder="Floor"
                  style={styles.input}
                  value={form.floor}
                  onChange={(e) => setForm({ ...form, floor: e.target.value })}
                />

                <input
                  type="text"
                  placeholder="Room"
                  style={styles.input}
                  value={form.room}
                  onChange={(e) => setForm({ ...form, room: e.target.value })}
                />
              </div>

              <div style={styles.formGrid}>
                <input
                  type="text"
                  placeholder="Cleaning Status"
                  style={styles.input}
                  value={form.cleaning_status}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      cleaning_status: e.target.value,
                    })
                  }
                />

                <input
                  type="text"
                  placeholder="Operational Status"
                  style={styles.input}
                  value={form.operational_status}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      operational_status: e.target.value,
                    })
                  }
                />
              </div>

              <div style={styles.formGrid}>
                <input
                  type="text"
                  placeholder="Maintenance Status"
                  style={styles.input}
                  value={form.maintenance_status}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      maintenance_status: e.target.value,
                    })
                  }
                />

                <input
                  type="date"
                  style={styles.input}
                  value={form.last_sanitized}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      last_sanitized: e.target.value,
                    })
                  }
                />
              </div>

              <div style={styles.buttonRow}>
                <button
                  onClick={() => {
                    setOpen(false);
                    resetForm();
                  }}
                  style={styles.secondaryButton}
                >
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

export default BedManagement;
