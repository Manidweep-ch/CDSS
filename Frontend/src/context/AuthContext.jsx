import { createContext, useState } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  // Initialize token synchronously from localStorage
  const [token, setToken] = useState(() => {
    try {
      const storedToken = localStorage.getItem("token");
      console.log("AuthContext initialized, token:", storedToken ? "exists" : "null");
      return storedToken;
    } catch (error) {
      console.error("Error reading token from localStorage:", error);
      return null;
    }
  });

  const login = (newToken) => {
    console.log("Login called with token");
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    console.log("Logout called");
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};