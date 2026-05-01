"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

interface UserState {
  age: number | null;
  location: string;
  is_citizen: boolean;
  is_resident: boolean;
  onboarded: boolean;
  token?: string;
}

interface UserContextType {
  user: UserState;
  updateUser: (data: Partial<UserState>) => void;
  initSession: () => Promise<void>;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<UserState>({
    age: null,
    location: "India",
    is_citizen: true,
    is_resident: true,
    onboarded: false,
    token: undefined
  });

  useEffect(() => {
    const saved = localStorage.getItem("eia-user-profile");
    const token = localStorage.getItem("eia-auth-token");
    
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setUser({ ...parsed, token: token || undefined });
      } catch (e) {
        console.error("Failed to parse user profile", e);
      }
    }
  }, []);

  const updateUser = (data: Partial<UserState>) => {
    const updated = { ...user, ...data, onboarded: true };
    setUser(updated);
    localStorage.setItem("eia-user-profile", JSON.stringify(updated));
  };

  const initSession = async () => {
    if (!user.onboarded) return;

    try {
      const res = await fetch("http://localhost:8000/api/session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          age: user.age,
          location: user.location,
          is_citizen: user.is_citizen,
          is_resident: user.is_resident
        })
      });
      const data = await res.json();
      if (data.access_token) {
        setUser(prev => ({ ...prev, token: data.access_token }));
        localStorage.setItem("eia-auth-token", data.access_token);
      }
    } catch (err) {
      console.error("Failed to initialize session", err);
    }
  };

  return (
    <UserContext.Provider value={{ user, updateUser, initSession }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) throw new Error("useUser must be used within a UserProvider");
  return context;
};
