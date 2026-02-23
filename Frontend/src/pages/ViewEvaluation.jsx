import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import DashboardLayout from "../components/DashboardLayout";
import MultiAnalyzerView from "../components/MultiAnalyzerView";
import axiosClient from "../api/axiosClient";
import "./ViewEvaluation.css";

function ViewEvaluation() {
  const { evaluationId } = useParams();
  const [evaluation, setEvaluation] = useState(null);
  const [extractedData, setExtractedData] = useState(null);
  const [availablePanels, setAvailablePanels] = useState([]);
  const [panelDetails, setPanelDetails] = useState({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadEvaluation();
  }, [evaluationId]);

  const loadEvaluation = async () => {
    try {
      const response = await axiosClient.get(`/evaluate/record/${evaluationId}`);
      const evalData = response.data;
      
      setEvaluation(evalData);
      setExtractedData(evalData.input_payload);
      setAvailablePanels(evalData.panels_run);
      
      const historicalPanelDetails = {};
      evalData.panels_run.forEach(panelName => {
        const panelResult = evalData.output_result[panelName];
        historicalPanelDetails[panelName] = {
          status: "available",
          description: `${panelName} Risk Analysis`,
          present_inputs: Object.keys(evalData.input_payload),
          missing_inputs: [],
          can_analyze: true,
          historical_result: {
            ...panelResult,
            evaluation_id: evalData.id
          },
          preloaded_result: panelResult
        };
      });
      
      setPanelDetails(historicalPanelDetails);
    } catch (err) {
      console.error("Failed to load evaluation:", err);
      alert(`Failed to load evaluation: ${err.response?.data?.detail || err.message}`);
      navigate("/dashboard/history");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="loading-state">
          <div className="spinner-large"></div>
          <p>Loading evaluation...</p>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="view-evaluation-page fade-in">
        <div className="page-header">
          <div>
            <h1>Evaluation #{evaluationId}</h1>
            <p>{evaluation && new Date(evaluation.timestamp).toLocaleString()}</p>
          </div>
          <button 
            className="btn-secondary"
            onClick={() => navigate("/dashboard/history")}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="19" y1="12" x2="5" y2="12"/>
              <polyline points="12 19 5 12 12 5"/>
            </svg>
            Back to History
          </button>
        </div>

        <div className="status-banner historical">
          <div className="status-content">
            <div className="status-icon">📋</div>
            <div>
              <h4>Historical Evaluation</h4>
              <p>Viewing past results • {availablePanels.length} panels analyzed</p>
            </div>
          </div>
        </div>

        {extractedData && (
          <MultiAnalyzerView
            extractedData={extractedData}
            availablePanels={availablePanels}
            panelDetails={panelDetails}
            unsupportedTests={[]}
            activeProfile={evaluation?.profile_id}
            historicalEvaluationId={parseInt(evaluationId)}
          />
        )}
      </div>
    </DashboardLayout>
  );
}

export default ViewEvaluation;
