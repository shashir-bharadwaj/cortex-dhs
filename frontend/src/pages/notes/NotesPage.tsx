import React, { useEffect, useState } from "react";
import { Button, Form, Input, Select, Spin, Tag, Typography, message } from "antd";
import { getPatientNotes, createPatientNote, ClinicalNote } from "../../api/notesApi";
import { getPatients } from "../../api/patientApi";
import { Patient } from "../../types/patient";
import PageHeader from "../../components/common/pageHeader";

const { Text, Title } = Typography;
const { TextArea } = Input;

const noteTypeColor: Record<string, string> = {
  progress: "blue",
  nursing: "green",
  order: "orange",
  handover: "purple",
};

const NotesPage: React.FC = () => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<number | null>(null);
  const [notes, setNotes] = useState<ClinicalNote[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    async function loadPatients() {
      try {
        const data = await getPatients();
        setPatients(data);
        if (data.length > 0) {
          setSelectedPatientId(data[0].id);
        }
      } catch {
        message.error("Failed to load patients");
      }
    }
    loadPatients();
  }, []);

  useEffect(() => {
    if (!selectedPatientId) return;
    async function loadNotes() {
      try {
        setLoading(true);
        const data = await getPatientNotes(selectedPatientId!);
        setNotes(data);
      } catch {
        message.error("Failed to load notes");
      } finally {
        setLoading(false);
      }
    }
    loadNotes();
  }, [selectedPatientId]);

  async function handleSubmit(values: { noteType: string; noteText: string }) {
    if (!selectedPatientId) return;
    try {
      setSubmitting(true);
      await createPatientNote(selectedPatientId, {
        noteType: values.noteType,
        noteText: values.noteText,
      });
      message.success("Note added");
      form.resetFields();
      const data = await getPatientNotes(selectedPatientId);
      setNotes(data);
    } catch {
      message.error("Failed to add note");
    } finally {
      setSubmitting(false);
    }
  }

  const selectedPatient = patients.find((p) => p.id === selectedPatientId);

  return (
    <div style={{ padding: 24 }}>
      <PageHeader title="Clinical Notes" />

      <div style={{ display: "flex", gap: 12, marginBottom: 24, alignItems: "center" }}>
        <Select
          style={{ width: 280 }}
          placeholder="Select patient"
          value={selectedPatientId}
          onChange={setSelectedPatientId}
          options={patients.map((p) => ({
            value: p.id,
            label: p.name,
          }))}
        />
      </div>

      {selectedPatient && (
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          style={{ marginBottom: 32 }}
          initialValues={{ noteType: "progress" }}
        >
          <Form.Item name="noteText">
            <TextArea
              rows={3}
              placeholder="Add a clinical note..."
              style={{ borderRadius: 8 }}
            />
          </Form.Item>
          <Form.Item name="noteType" style={{ display: "none" }}>
            <Select
              options={[
                { value: "progress", label: "Progress" },
                { value: "nursing", label: "Nursing" },
                { value: "order", label: "Order" },
                { value: "handover", label: "Handover" },
              ]}
            />
          </Form.Item>
          <Button type="primary" htmlType="submit" loading={submitting}>
            Add Note
          </Button>
        </Form>
      )}

      {loading ? (
        <div style={{ display: "flex", justifyContent: "center", padding: 48 }}>
          <Spin />
        </div>
      ) : (
        <div>
          {notes.map((note) => (
            <div
              key={note.id}
              style={{
                borderBottom: "1px solid #f0f0f0",
                paddingBottom: 16,
                marginBottom: 16,
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <Text strong>{note.authorName}</Text>
                  <Tag color={noteTypeColor[note.noteType] ?? "default"}>{note.noteType}</Tag>
                </div>
                <Text type="secondary" style={{ fontSize: 12 }}>
                  {new Date(note.createdAt).toLocaleString()}
                </Text>
              </div>
              <Text>{note.noteText}</Text>
            </div>
          ))}
          {notes.length === 0 && !loading && (
            <div style={{ textAlign: "center", padding: 48, color: "#999" }}>
              No notes for this patient
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default NotesPage;
