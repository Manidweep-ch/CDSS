import { useState, useEffect } from "react";
import AnalyzerPanel from "./AnalyzerPanel";
import axiosClient from "../api/axiosClient";
import "./MultiAnalyzerView.css";

function MultiAnalyzerView({ 
  extractedData, 
  availablePanels, 
  panelDetails, 
  unsupportedTests,
  activeProfile,
  historicalEvaluationId
}) {
  const [analyzingAll, setAnalyzingAll] = useState(false);
  const [allResults, setAllResults] = useState(null);
  const [evaluationId, setEvaluationId] = useState(historicalEvaluationId);
  const [showGlobalChat, setShowGlobalChat] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [sessionId, setSessionId] = useState(null);

  // Load historical results and chat if viewing history
  useEffect(() => {
    if (historicalEvaluationId) {
      // Extract results from panel details
      const results = {};
      availablePanels.forEach(panelName => {
        if (panelDetails[panelName]?.preloaded_result) {
          results[panelName] = panelDetails[panelName].preloaded_result;
        }
      });
      setAllResults(results);
      setEvaluationId(historicalEvaluationId);

      // Load existing chat history
      loadChatHistory(historicalEvaluationId);
    }
  }, [historicalEvaluationId]);

  const loadChatHistory = async (evalId) => {
    try {
      const response = await axiosClient.get(`/chat/${evalId}`);
      const sessions = response.data;

      // Find global session
      const globalSession = sessions.find(s => s.session_type === "global");

      if (globalSession && globalSession.messages.length > 0) {
        setSessionId(globalSession.session_id);
        setChatMessages(globalSession.messages.map(m => ({
          role: m.role,
          message: m.message
        })));
        console.log("Loaded global chat history:", globalSession.messages.length, "messages");
      } else {
        // Create new session
        const chatResponse = await axiosClient.post("/chat/start", {
          evaluation_id: evalId,
          session_type: "global",
          panel_name: null
        });
        setSessionId(chatResponse.data.session_id);
      }
    } catch (err) {
      console.error("Failed to load chat history:", err);
    }
  };

  const analyzeAll = async () => {
    setAnalyzingAll(true);

    try {
      const response = await axiosClient.post(
        `/evaluate/${activeProfile}`,
        {
          panels: availablePanels,
          data: extractedData
        }
      );

      setAllResults(response.data.results);
      setEvaluationId(response.data.evaluation_id);

      // Start global chat session for the entire report
      try {
        const chatResponse = await axiosClient.post("/chat/start", {
          evaluation_id: response.data.evaluation_id,
          session_type: "global",
          panel_name: null
        });
        setSessionId(chatResponse.data.session_id);
      } catch (err) {
        console.error("Failed to start chat:", err);
      }

      alert(`Successfully analyzed ${availablePanels.length} panels!`);
    } catch (err) {
      alert(`Batch analysis failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setAnalyzingAll(false);
    }
  };

  const sendChatMessage = async () => {
    if (!chatInput.trim() || !sessionId) return;

    const userMessage = chatInput;
    setChatMessages([...chatMessages, { role: "user", message: userMessage }]);
    setChatInput("");

    try {
      const response = await axiosClient.post("/chat/message", {
        session_id: sessionId,
        message: userMessage
      });

      setChatMessages(prev => [...prev, { 
        role: "assistant", 
        message: response.data.ai_response 
      }]);
    } catch (err) {
      alert("Chat message failed: " + (err.response?.data?.detail || err.message));
      console.error("Chat error:", err);
    }
  };

  return (
    <div className="multi-analyzer-container">
      <div className="analyzer-header">
        <h3>Available Analyzers ({availablePanels.length})</h3>
        
        {availablePanels.length > 0 && (
          <button
            onClick={analyzeAll}
            disabled={analyzingAll}
            className="btn-primary"
          >
            {analyzingAll ? "Analyzing All..." : "🚀 Analyze All"}
          </button>
        )}
      </div>

      {availablePanels.length === 0 && (
        <p className="empty-message">
          No analyzers available for the detected tests.
        </p>
      )}

      {/* Show global results and chat after Analyze All */}
      {allResults && (
        <div className="results-summary">
          <h4>
            ✅ All Panels Analyzed
          </h4>
          
          {Object.entries(allResults).map(([panelName, result]) => (
            <div key={panelName} className="result-item-card">
              <strong>{panelName}:</strong> <span>{result.final_decision}</span>
              {result.confidence && <span> ({(result.confidence * 100).toFixed(1)}% confidence)</span>}
            </div>
          ))}

          <button
            onClick={() => setShowGlobalChat(!showGlobalChat)}
            className="chat-toggle-btn"
          >
            {showGlobalChat ? "Hide" : "Show"} Report Chat 💬
          </button>

          {showGlobalChat && (
            <div className="chat-container">
              {chatMessages.length > 0 && (
                <div className="chat-message-count">
                  💬 {chatMessages.length} message{chatMessages.length !== 1 ? 's' : ''} about this report
                </div>
              )}

              <div className="chat-messages">
                {chatMessages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`chat-message ${msg.role}`}
                  >
                    <strong>
                      {msg.role === "user" ? "You" : "AI Assistant"}:
                    </strong>
                    <div className="chat-message-content">
                      {msg.message}
                    </div>
                  </div>
                ))}
              </div>

              <div className="chat-input-container">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && sendChatMessage()}
                  placeholder="Ask about the overall report..."
                  className="chat-input"
                />
                <button
                  onClick={sendChatMessage}
                  disabled={!chatInput.trim() || !sessionId}
                  className="chat-send-btn"
                >
                  Send
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Individual Analyzers */}
      {["Diabetes", "Cardiovascular", "Kidney"].map(panelName => (
        <AnalyzerPanel
          key={panelName}
          panelName={panelName}
          panelDetail={panelDetails[panelName]}
          extractedData={extractedData}
          activeProfile={activeProfile}
          onAnalysisComplete={() => {}}
          preloadedResult={allResults?.[panelName]}
        />
      ))}

      {/* Unsupported Tests */}
      {unsupportedTests && unsupportedTests.length > 0 && (
        <div className="unsupported-tests">
          <h4>
            ⚠️ Tests Without Analyzers
          </h4>
          <p>
            The following tests were detected but don't have analysis models yet:
          </p>
          <ul>
            {unsupportedTests.map(test => (
              <li key={test}>
                {test}: {extractedData[test]}
              </li>
            ))}
          </ul>
          <p className="note">
            These analyzers are under development and will be available soon.
          </p>
        </div>
      )}
    </div>
  );
}

export default MultiAnalyzerView;
