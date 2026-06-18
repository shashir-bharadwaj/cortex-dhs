import React, { useEffect, useState } from "react";
import { Button, Card, Col, Row, Spin, Tag, Typography, message } from "antd";
import { CheckOutlined, ClockCircleOutlined } from "@ant-design/icons";
import { getNurseTasks, completeNurseTask } from "../../api/nurseTaskApi";
import { NurseTask, NurseTaskSummary } from "../../types/nurseTask";
import PageHeader from "../../components/common/pageHeader";

const { Text } = Typography;

const statusColor: Record<string, string> = {
  pending: "orange",
  in_progress: "blue",
  completed: "green",
};

const TasksPage: React.FC = () => {
  const [summary, setSummary] = useState<NurseTaskSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [completing, setCompleting] = useState<number | null>(null);

  async function fetchTasks() {
    try {
      setLoading(true);
      const data = await getNurseTasks();
      setSummary(data);
    } catch {
      message.error("Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchTasks();
  }, []);

  async function handleComplete(taskId: number) {
    try {
      setCompleting(taskId);
      await completeNurseTask(taskId);
      message.success("Task marked as completed");
      fetchTasks();
    } catch {
      message.error("Failed to complete task");
    } finally {
      setCompleting(null);
    }
  }

  if (loading) {
    return (
      <div style={{ display: "flex", justifyContent: "center", padding: 48 }}>
        <Spin size="large" />
      </div>
    );
  }

  const pending = summary?.tasks.filter((t) => t.status !== "completed") ?? [];
  const completed = summary?.tasks.filter((t) => t.status === "completed") ?? [];

  return (
    <div style={{ padding: 24 }}>
      <PageHeader title="Nurse Task List" />
      <Text type="secondary" style={{ display: "block", marginBottom: 24 }}>
        Assigned nursing tasks for current shift
      </Text>

      {summary && (
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={8}>
            <Card style={{ textAlign: "center" }}>
              <div style={{ fontSize: 32, fontWeight: 700 }}>{summary.total}</div>
              <Text type="secondary">Total Tasks</Text>
            </Card>
          </Col>
          <Col span={8}>
            <Card style={{ textAlign: "center" }}>
              <div style={{ fontSize: 32, fontWeight: 700 }}>{summary.pending}</div>
              <Text type="secondary">Pending</Text>
            </Card>
          </Col>
          <Col span={8}>
            <Card style={{ textAlign: "center" }}>
              <div style={{ fontSize: 32, fontWeight: 700 }}>{summary.completed}</div>
              <Text type="secondary">Completed</Text>
            </Card>
          </Col>
        </Row>
      )}

      {pending.length > 0 && (
        <>
          <Text strong style={{ display: "block", marginBottom: 12, color: "#888" }}>
            PENDING
          </Text>
          {pending.map((task) => (
            <TaskRow
              key={task.id}
              task={task}
              onComplete={handleComplete}
              completing={completing === task.id}
            />
          ))}
        </>
      )}

      {completed.length > 0 && (
        <>
          <Text strong style={{ display: "block", marginTop: 24, marginBottom: 12, color: "#888" }}>
            COMPLETED
          </Text>
          {completed.map((task) => (
            <TaskRow
              key={task.id}
              task={task}
              onComplete={handleComplete}
              completing={completing === task.id}
            />
          ))}
        </>
      )}

      {(summary?.tasks.length ?? 0) === 0 && (
        <div style={{ textAlign: "center", padding: 48, color: "#999" }}>
          No tasks assigned for this shift
        </div>
      )}
    </div>
  );
};

interface TaskRowProps {
  task: NurseTask;
  onComplete: (id: number) => void;
  completing: boolean;
}

const TaskRow: React.FC<TaskRowProps> = ({ task, onComplete, completing }) => {
  return (
    <Card
      style={{ marginBottom: 8, borderRadius: 8 }}
      bodyStyle={{ padding: "12px 16px" }}
    >
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          {task.status !== "completed" ? (
            <Button
              shape="circle"
              size="small"
              loading={completing}
              icon={<CheckOutlined />}
              onClick={() => onComplete(task.id)}
            />
          ) : (
            <CheckOutlined style={{ color: "green", fontSize: 18 }} />
          )}
          <div>
            <Text strong>{task.title}</Text>
            <div>
              <Text type="secondary" style={{ fontSize: 12 }}>
                {task.patientName} &nbsp;·&nbsp; {task.bedLabel}
              </Text>
            </div>
          </div>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <Tag color={statusColor[task.status]}>{task.status.replace("_", " ")}</Tag>
          {task.dueTime && (
            <Text type="secondary" style={{ fontSize: 12 }}>
              <ClockCircleOutlined />{" "}
              {new Date(task.dueTime).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </Text>
          )}
        </div>
      </div>
    </Card>
  );
};

export default TasksPage;
