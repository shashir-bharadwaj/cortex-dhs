import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Form, Input, Button, Typography, message } from "antd";
import { useAuth } from "../../auth/AuthContext";
import { loginApi } from "../../api";

const { Text } = Typography;

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values: { email: string; password: string }) => {
    setLoading(true);
    try {
      const result = await loginApi(values.email, values.password);
      login(result.token, result.user);
      localStorage.setItem("role", String(result.user.userId));
      localStorage.setItem("token", result.token);
      navigate("/dashboard");
    } catch (err: any) {
      message.error(err?.response?.data?.detail || "Invalid credentials");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#e8e8ed",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          width: 440,
          borderRadius: 18,
          overflow: "hidden",
          boxShadow: "0 8px 40px rgba(0,0,0,0.18)",
        }}
      >
        {/* Purple header section */}
        <div
          style={{
            background: "#5b2be0",
            padding: "38px 40px 32px",
            textAlign: "center",
          }}
        >
          <div
            style={{
              fontSize: 28,
              fontWeight: 800,
              color: "#fff",
              letterSpacing: 1,
              marginBottom: 6,
            }}
          >
            BPL CNS
          </div>
          <div style={{ fontSize: 14, color: "rgba(255,255,255,0.85)", marginBottom: 12 }}>
            Central Nursing Station – ICU Monitoring
          </div>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 6 }}>
            <span
              style={{
                width: 8,
                height: 8,
                borderRadius: "50%",
                background: "#00e5a0",
                display: "inline-block",
              }}
            />
            <span style={{ fontSize: 13, color: "#00e5a0", fontWeight: 500 }}>
              System Connected
            </span>
          </div>
        </div>

        {/* White form section */}
        <div style={{ background: "#fff", padding: "32px 40px 28px" }}>
          <Form
            initialValues={{ email: "nurse@cortex.com", password: "nurse" }}
            onFinish={handleSubmit}
            layout="vertical"
            requiredMark={false}
          >
            <Form.Item
              name="email"
              label={
                <span style={{ fontSize: 13, fontWeight: 600, color: "#333" }}>Email ID</span>
              }
              rules={[{ required: true, message: "Email is required" }]}
            >
              <Input
                placeholder="nurse@cortex.com"
                size="large"
                style={{
                  borderRadius: 8,
                  border: "1.5px solid #e0e0e0",
                  background: "#f7f7fb",
                  fontSize: 14,
                }}
              />
            </Form.Item>

            <Form.Item
              name="password"
              label={
                <span style={{ fontSize: 13, fontWeight: 600, color: "#333" }}>Password</span>
              }
              rules={[{ required: true, message: "Password is required" }]}
              style={{ marginBottom: 6 }}
            >
              <Input.Password
                size="large"
                style={{
                  borderRadius: 8,
                  border: "1.5px solid #e0e0e0",
                  background: "#f7f7fb",
                  fontSize: 14,
                }}
              />
            </Form.Item>

            {/* Forgot Password */}
            <div style={{ textAlign: "right", marginBottom: 20 }}>
              <a
                href="#"
                style={{ fontSize: 13, color: "#5b2be0", textDecoration: "none" }}
                onClick={(e) => e.preventDefault()}
              >
                Forgot Password?
              </a>
            </div>

            <Form.Item style={{ marginBottom: 16 }}>
              <Button
                type="primary"
                htmlType="submit"
                loading={loading}
                block
                size="large"
                style={{
                  background: "#5b2be0",
                  borderColor: "#5b2be0",
                  borderRadius: 8,
                  height: 48,
                  fontSize: 16,
                  fontWeight: 600,
                }}
              >
                Sign In
              </Button>
            </Form.Item>
          </Form>

          {/* Sign up footer */}
          <div style={{ textAlign: "center", marginTop: 4 }}>
            <Text style={{ fontSize: 13, color: "#888" }}>
              Don't have an account?{" "}
              <a
                href="#"
                style={{ color: "#5b2be0", fontWeight: 600, textDecoration: "none" }}
                onClick={(e) => e.preventDefault()}
              >
                Sign Up
              </a>
            </Text>
          </div>
        </div>
      </div>
    </div>
  );
}
