import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../components/DashboardLayout";
import PDFUploader from "../components/PDFUploader";
import MultiAnalyzerView from "../components/MultiAnalyzerView";
import axiosClient from "../api/axiosClient";
import "./Analyze.css";

function Analyze() {
  const [activeProfile, setActiveProfile] = useState(null);
  const [profileName, setProfileName] = useState("");
  const [extractedData, setExtractedData] = useState(null);
  const [availablePanels, setAvailablePanels] = useState([]);
  const [panelDetails, setPanelDetails] = useState({});
  const [unsupportedTests, setUnsupportedTests] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const profileId = localStorage.getItem("activeProfile");
    if (!profileId) {
      navigate("/dashboard/profiles");
      return;
    }
    setActiveProfile(parseInt(profileId));
    fetchProfileName(profileId);
  }, []);

  const fetchProfileName = async (profileId) => {
    try {
      const response = await axiosClient.get(`/profiles/${profileId}`);
      setProfileName(response.data.profile_name);
    } catch (err) {
      console.error("Failed to fetch profile:", err);
    }
  };

  const handleExtractionComplete = (data) => {
    setExtractedData(data.extracted_data);
    setAvailablePanels(data.available_panels);
    setPanelDetails(data.panel_details);
    setUnsupportedTests(data.unsupported_tests);
  };

  const resetUpload = () => {
    setExtractedData(null);
    setAvailablePanels([]);
    setPanelDetails({});
    setUnsupportedTests([]);
  };

  return (
    <DashboardLayout>
      <div className="analyze-page fade-in">
        <div className="page-header">
          <div>
            <h1>Medical Analysis</h1>
            <p>Upload and analyze lab reports for {profileName || "selected patient"}</p>
          </div>
          <button 
            className="btn-secondary"
            onClick={() => navigate("/dashboard/profiles")}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="19" y1="12" x2="5" y2="12"/>
              <polyline points="12 19 5 12 12 5"/>
            </svg>
            Change Profile
          </button>
        </div>

        {!extractedData ? (
          <div className="upload-section">
            <PDFUploader onExtractionComplete={handleExtractionComplete} />
          </div>
        ) : (
          <>
            <div className="status-banner success">
              <div className="status-content">
                <div className="status-icon">✅</div>
                <div>
                  <h4>PDF Processed Successfully</h4>
                  <p>Found {Object.keys(extractedData).length} test results • {availablePanels.length} analyzers available</p>
                </div>
              </div>
              <button onClick={resetUpload} className="btn-secondary">
                Upload New PDF
              </button>
            </div>

            <MultiAnalyzerView
              extractedData={extractedData}
              availablePanels={availablePanels}
              panelDetails={panelDetails}
              unsupportedTests={unsupportedTests}
              activeProfile={activeProfile}
              historicalEvaluationId={null}
            />
          </>
        )}
      </div>
    </DashboardLayout>
  );
}

export default Analyze;
