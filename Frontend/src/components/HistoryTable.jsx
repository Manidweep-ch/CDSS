import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";

function HistoryTable({ activeProfile, onLoadEvaluation }) {
  const [history, setHistory] = useState([]);

  const fetchHistory = async () => {
    if (!activeProfile) {
      setHistory([]);
      return;
    }

    try {
      console.log("Fetching history for profile ID:", activeProfile);
      const response = await axiosClient.get(
        `/evaluate/history/${activeProfile}`
      );
      console.log("History response:", response.data);
      setHistory(response.data);
    } catch (err) {
      console.error("Failed to fetch history:", err);
      if (err.response?.status === 404) {
        setHistory([]);
      }
    }
  };

  useEffect(() => {
    console.log("HistoryTable: activeProfile changed to:", activeProfile);
    fetchHistory();
  }, [activeProfile]);

  const deleteEvaluation = async (evaluationId) => {
    if (!confirm("Are you sure you want to delete this evaluation?")) {
      return;
    }

    try {
      await axiosClient.delete(`/evaluate/record/${evaluationId}`);
      await fetchHistory(); // Refresh list
      alert("Evaluation deleted successfully");
    } catch (err) {
      console.error("Failed to delete evaluation:", err);
      alert(`Failed to delete evaluation: ${err.response?.data?.detail || err.message}`);
    }
  };

  return (
    <div style={{ marginTop: "30px", padding: "15px", border: "1px solid #ddd", borderRadius: "8px" }}>
      <h3>📋 Evaluation History</h3>

      {!activeProfile && (
        <p style={{ color: "#999", fontStyle: "italic" }}>Select a profile to view history</p>
      )}

      {activeProfile && history.length === 0 && (
        <p style={{ color: "#999", fontStyle: "italic" }}>No evaluations yet for this profile.</p>
      )}

      {history.map((item) => (
        <div key={item.id}
          style={{
            border: "1px solid #ddd",
            padding: "12px",
            margin: "10px 0",
            borderRadius: "8px",
            backgroundColor: "#f9f9f9"
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <p style={{ margin: "0 0 5px 0" }}>
                <strong>ID:</strong> {item.id} | <strong>Date:</strong> {new Date(item.timestamp).toLocaleString()}
              </p>
              <p style={{ margin: "0", fontSize: "14px", color: "#666" }}>
                <strong>Panels:</strong> {item.panels_run?.join(", ")}
              </p>
            </div>
            <div style={{ display: "flex", gap: "5px" }}>
              <button 
                onClick={() => onLoadEvaluation(item.id)}
                style={{
                  padding: "8px 16px",
                  backgroundColor: "#2196F3",
                  color: "white",
                  border: "none",
                  borderRadius: "4px",
                  cursor: "pointer"
                }}
              >
                📄 View Report
              </button>
              <button 
                onClick={() => deleteEvaluation(item.id)}
                style={{
                  padding: "8px 16px",
                  backgroundColor: "#f44336",
                  color: "white",
                  border: "none",
                  borderRadius: "4px",
                  cursor: "pointer"
                }}
              >
                🗑️ Delete
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default HistoryTable;