"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

interface UserState {
  age: number | null;
  location: string;
  is_citizen: boolean;
  is_resident: boolean;
  onboarded: boolean;
}

interface UserContextType {
  user: UserState;
  updateUser: (data: Partial<UserState>) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<UserState>({
    age: null,
    location: "India",
    is_citizen: true,
    is_resident: true,
    onboarded: false
  });

  useEffect(() => {
    const saved = localStorage.getItem("eia-user-profile");
    if (saved) {
      try {
        setUser(JSON.parse(saved));
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

  return (
    <UserContext.Provider value={{ user, updateUser }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) throw new Error("useUser must be used within a UserProvider");
  return context;
};
