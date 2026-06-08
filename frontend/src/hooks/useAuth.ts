import { useState, useEffect } from 'react';

export interface AuthContext {
  token: string | null;
  setToken: (token: string | null) => void;
}

export function useAuth(): AuthContext {
  const [token, setTokenState] = useState<string | null>(() => {
    return localStorage.getItem('token');
  });
  const setToken = (t: string | null) => {
    if (t) localStorage.setItem('token', t);
    else localStorage.removeItem('token');
    setTokenState(t);
  };
  return { token, setToken };
}