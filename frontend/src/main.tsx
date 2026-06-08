import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { ConfigProvider } from "antd";

import App from "./App";
import { AuthProvider } from "./auth/AuthContext";
// Ant Design uses CSS-in-JS but we need base styles imported above

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <ConfigProvider>
          <App />
        </ConfigProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);

// Register the service worker for offline support (PWA)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/sw.js')
      .catch((registrationError) => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}