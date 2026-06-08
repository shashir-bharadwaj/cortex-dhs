import React, { createContext, useContext, useEffect, useMemo, useState } from "react";

type AuthContextType = {
  isAuthenticated: boolean;
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const savedToken = localStorage.getItem("access_token");
    if (savedToken) {
      setToken(savedToken);
    }
  }, []);

  const login = (newToken: string) => {
    console.log("Saving token to auth state");
    localStorage.setItem("access_token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
  };

  const value = useMemo(
    () => ({
      token,
      isAuthenticated: !!token,
      login,
      logout,
    }),
    [token]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};