import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "./context/AuthContext";
import { ThemeProvider } from "./context/ThemeContext";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import DashboardHome from "./pages/DashboardHome";
import Profiles from "./pages/Profiles";
import Analyze from "./pages/Analyze";
import History from "./pages/History";
import ViewEvaluation from "./pages/ViewEvaluation";

function PrivateRoute({ children }) {
  const { token } = useContext(AuthContext);
  return token ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <DashboardHome />
              </PrivateRoute>
            }
          />
          <Route
            path="/dashboard/home"
            element={
              <PrivateRoute>
                <DashboardHome />
              </PrivateRoute>
            }
          />
          <Route
            path="/dashboard/profiles"
            element={
              <PrivateRoute>
                <Profiles />
              </PrivateRoute>
            }
          />
          <Route
            path="/dashboard/analyze"
            element={
              <PrivateRoute>
                <Analyze />
              </PrivateRoute>
            }
          />
          <Route
            path="/dashboard/history"
            element={
              <PrivateRoute>
                <History />
              </PrivateRoute>
            }
          />
          <Route
            path="/dashboard/view/:evaluationId"
            element={
              <PrivateRoute>
                <ViewEvaluation />
              </PrivateRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
