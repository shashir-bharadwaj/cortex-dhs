import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

type Props = {
  children: React.ReactNode;
};

const ProtectedRoute: React.FC<Props> = ({ children }) => {
  const { isAuthenticated } = useAuth();

  console.log("ProtectedRoute isAuthenticated:", isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;