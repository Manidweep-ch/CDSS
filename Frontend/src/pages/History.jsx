import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../components/DashboardLayout";
import axiosClient from "../api/axiosClient";
import "./History.css";

function History() {
  const [profiles, setProfiles] = useState([]);
  const [selectedProfile, setSelectedProfile] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchProfiles();
  }, []);

  useEffect(() => {
    if (selectedProfile) {
      fetchHistory(selectedProfile);
    }
  }, [selectedProfile]);

  const fetchProfiles = async () => {
    try {
      const response = await axiosClient.get("/profiles/");
      setProfiles(response.data);
      if (response.data.length > 0) {
        setSelectedProfile(response.data[0].id);
      }
    } catch (err) {
      console.error("Failed to fetch profiles:", err);
    }
  };

  const fetchHistory = async (profileId) => {
    setLoading(true);
    try {
      const response = await axiosClient.get(`/evaluate/history/${profileId}`);
      setHistory(response.data);
    } catch (err) {
      console.error("Failed to fetch history:", err);
      setHistory([]);
    } finally {
      setLoading(false);
    }
  };

  const deleteEvaluation = async (evaluationId) => {
    if (!confirm("Are you sure you want to delete this evaluation?")) {
      return;
    }

    try {
      await axiosClient.delete(`/evaluate/record/${evaluationId}`);
      fetchHistory(selectedProfile);
      alert("Evaluation deleted successfully");
    } catch (err) {
      console.error("Failed to delete evaluation:", err);
      alert(`Failed to delete: ${err.response?.data?.detail || err.message}`);
    }
  };

  const viewEvaluation = (evaluationId) => {
    navigate(`/dashboard/view/${evaluationId}`);
  };

  return (
    <DashboardLayout>
      <div className="history-page fade-in">
        <div className="page-header">
          <div>
            <h1>Evaluation History</h1>
            <p>View and manage past medical evaluations</p>
          </div>
        </div>

        <div className="profile-selector">
          <label>Select Profile:</label>
          <select 
            value={selectedProfile || ""} 
            onChange={(e) => setSelectedProfile(parseInt(e.target.value))}
          >
            {profiles.map(profile => (
              <option key={profile.id} value={profile.id}>
                {profile.profile_name}
              </option>
            ))}
          </select>
        </div>

        {loading ? (
          <div className="loading-state">
            <div className="spinner-large"></div>
            <p>Loading history...</p>
          </div>
        ) : history.length === 0 ? (
          <div className="empty-state">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10 9 9 9 8 9"/>
            </svg>
            <h3>No evaluations yet</h3>
            <p>Upload a lab report to create your first evaluation</p>
          </div>
        ) : (
          <div className="history-grid">
            {history.map((item) => (
              <div key={item.id} className="history-card">
                <div className="card-header">
                  <div className="card-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                    </svg>
                  </div>
                  <div className="card-meta">
                    <h4>Evaluation #{item.id}</h4>
                    <p>{new Date(item.timestamp).toLocaleString()}</p>
                  </div>
                </div>
                <div className="card-content">
                  <div className="panels-list">
                    {item.panels_run?.map(panel => (
                      <span key={panel} className="panel-badge">{panel}</span>
                    ))}
                  </div>
                </div>
                <div className="card-actions">
                  <button 
                    className="btn-view"
                    onClick={() => viewEvaluation(item.id)}
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                    View Report
                  </button>
                  <button 
                    className="btn-delete"
                    onClick={() => deleteEvaluation(item.id)}
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <polyline points="3 6 5 6 21 6"/>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                    </svg>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default History;
