import { useState, useEffect } from "react";
import ProfileManager from "../components/ProfileManager";
import PDFUploader from "../components/PDFUploader";
import MultiAnalyzerView from "../components/MultiAnalyzerView";
import HistoryTable from "../components/HistoryTable";
import axiosClient from "../api/axiosClient";
import "./Dashboard.css";

function Dashboard() {
  const [activeProfile, setActiveProfile] = useState(null);
  const [extractedData, setExtractedData] = useState(null);
  const [availablePanels, setAvailablePanels] = useState([]);
  const [panelDetails, setPanelDetails] = useState({});
  const [unsupportedTests, setUnsupportedTests] = useState([]);
  const [showManualInput, setShowManualInput] = useState(false);
  const [isHistoricalView, setIsHistoricalView] = useState(false);
  const [historicalEvaluationId, setHistoricalEvaluationId] = useState(null);

  useEffect(() => {
    console.log("Dashboard: activeProfile changed to:", activeProfile);
    setExtractedData(null);
    setAvailablePanels([]);
    setPanelDetails({});
    setUnsupportedTests([]);
    setIsHistoricalView(false);
    setHistoricalEvaluationId(null);
  }, [activeProfile]);

  const handleExtractionComplete = (data) => {
    setExtractedData(data.extracted_data);
    setAvailablePanels(data.available_panels);
    setPanelDetails(data.panel_details);
    setUnsupportedTests(data.unsupported_tests);
    setIsHistoricalView(false);
  };

  const loadEvaluation = async (evaluationId) => {
    try {
      const response = await axiosClient.get(`/evaluate/record/${evaluationId}`);
      const evaluation = response.data;
      
      setExtractedData(evaluation.input_payload);
      setAvailablePanels(evaluation.panels_run);
      
      const historicalPanelDetails = {};
      evaluation.panels_run.forEach(panelName => {
        const panelResult = evaluation.output_result[panelName];
        historicalPanelDetails[panelName] = {
          status: "available",
          description: `${panelName} Risk Analysis (Historical)`,
          present_inputs: Object.keys(evaluation.input_payload),
          missing_inputs: [],
          can_analyze: true,
          historical_result: {
            ...panelResult,
            evaluation_id: evaluation.id
          },
          preloaded_result: panelResult
        };
      });
      
      setPanelDetails(historicalPanelDetails);
      setUnsupportedTests([]);
      setIsHistoricalView(true);
      setHistoricalEvaluationId(evaluation.id);
    } catch (err) {
      console.error("Failed to load evaluation:", err);
      alert(`Failed to load evaluation: ${err.response?.data?.detail || err.message}`);
    }
  };

  const resetUpload = () => {
    setExtractedData(null);
    setAvailablePanels([]);
    setPanelDetails({});
    setUnsupportedTests([]);
    setIsHistoricalView(false);
    setHistoricalEvaluationId(null);
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header fade-in">
        <div className="header-content">
          <div className="header-title">
            <div className="header-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
              </svg>
            </div>
            <div>
              <h1>Medical Analysis Dashboard</h1>
              <p>Intelligent Clinical Decision Support System</p>
            </div>
          </div>
          <button 
            className="btn-logout"
            onClick={() => {
              localStorage.removeItem("token");
              window.location.href = "/login";
            }}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard-main">
        <ProfileManager 
          onProfileSelect={setActiveProfile} 
          activeProfile={activeProfile}
        />

        {activeProfile && (
          <>
            {!extractedData ? (
              <div className="upload-section slide-in">
                <PDFUploader onExtractionComplete={handleExtractionComplete} />
              </div>
            ) : (
              <>
                <div className={`status-banner ${isHistoricalView ? 'historical' : 'success'} fade-in`}>
                  <div className="status-content">
                    <div className="status-icon">
                      {isHistoricalView ? "📋" : "✅"}
                    </div>
                    <div>
                      <h4>{isHistoricalView ? "Historical Evaluation" : "PDF Processed Successfully"}</h4>
                      <p>
                        {isHistoricalView 
                          ? `Viewing past results • ${availablePanels.length} panels analyzed`
                          : `Found ${Object.keys(extractedData).length} test results • ${availablePanels.length} analyzers available`
                        }
                      </p>
                    </div>
                  </div>
                  <button onClick={resetUpload} className="btn-secondary">
                    {isHistoricalView ? "Close History" : "Upload New PDF"}
                  </button>
                </div>

                <MultiAnalyzerView
                  extractedData={extractedData}
                  availablePanels={availablePanels}
                  panelDetails={panelDetails}
                  unsupportedTests={unsupportedTests}
                  activeProfile={activeProfile}
                  historicalEvaluationId={historicalEvaluationId}
                />
              </>
            )}

            <HistoryTable
              activeProfile={activeProfile}
              onLoadEvaluation={loadEvaluation}
            />
          </>
        )}
      </main>
    </div>
  );
}

export default Dashboard;
