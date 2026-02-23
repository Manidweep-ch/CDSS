import { useState } from "react";
import axiosClient from "../api/axiosClient";
import "./AnalyzerPanel.css";

function AnalyzerPanel({ 
  panelName, 
  panelDetail, 
  extractedData, 
  activeProfile,
  onAnalysisComplete,
  preloadedResult
}) {
  const [analyzing, setAnalyzing] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [result, setResult] = useState(preloadedResult || null);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [sessionId, setSessionId] = useState(null);

  // Update result when preloadedResult changes
  useState(() => {
    if (preloadedResult) {
      setResult(preloadedResult);
    }
  }, [preloadedResult]);

  // Update result when preloadedResult changes
  useState(() => {
    if (preloadedResult) {
      setResult(preloadedResult);
    }
  }, [preloadedResult]);

  const runAnalysis = async () => {
    // If historical result exists, just display it
    if (panelDetail?.historical_result) {
      setResult(panelDetail.historical_result);
      
      // Try to load existing chat history for this evaluation
      const evalId = panelDetail.historical_result.evaluation_id;
      if (evalId) {
        try {
          // First, try to get existing chat sessions
          const chatHistoryResponse = await axiosClient.get(`/chat/${evalId}`);
          const sessions = chatHistoryResponse.data;
          
          // Find the session for this panel
          const panelSession = sessions.find(s => 
            s.session_type === "panel" && s.panel_name === panelName
          );
          
          if (panelSession && panelSession.messages.length > 0) {
            // Load existing chat messages
            setSessionId(panelSession.session_id);
            setChatMessages(panelSession.messages.map(m => ({
              role: m.role,
              message: m.message
            })));
            console.log("Loaded existing chat history:", panelSession.messages.length, "messages");
          } else {
            // No existing chat, create new session
            const chatResponse = await axiosClient.post("/chat/start", {
              evaluation_id: evalId,
              session_type: "panel",
              panel_name: panelName
            });
            setSessionId(chatResponse.data.session_id);
          }
        } catch (err) {
          console.error("Failed to load chat history:", err);
          // If loading history fails, try to create new session
          try {
            const chatResponse = await axiosClient.post("/chat/start", {
              evaluation_id: evalId,
              session_type: "panel",
              panel_name: panelName
            });
            setSessionId(chatResponse.data.session_id);
          } catch (err2) {
            console.error("Failed to start new chat session:", err2);
          }
        }
      }
      return;
    }
    
    setAnalyzing(true);
    
    try {
      console.log("Starting analysis for", panelName);
      console.log("Profile ID:", activeProfile);
      console.log("Extracted data:", extractedData);
      
      const response = await axiosClient.post(
        `/evaluate/${activeProfile}`,
        {
          panels: [panelName],
          data: extractedData
        }
      );

      console.log("Analysis response:", response.data);

      const panelResult = response.data.results[panelName];
      console.log("Panel result:", panelResult);
      
      setResult(panelResult);
      onAnalysisComplete(panelName, panelResult);

      // Start chat session
      const chatResponse = await axiosClient.post("/chat/start", {
        evaluation_id: response.data.evaluation_id,
        session_type: "panel",
        panel_name: panelName
      });

      console.log("Chat session created:", chatResponse.data);
      setSessionId(chatResponse.data.session_id);
      
    } catch (err) {
      console.error("Analysis error:", err);
      alert(`Analysis failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setAnalyzing(false);
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

      // Add AI response to chat
      setChatMessages(prev => [...prev, { 
        role: "assistant", 
        message: response.data.ai_response 
      }]);
      
    } catch (err) {
      alert("Chat message failed: " + (err.response?.data?.detail || err.message));
      console.error("Chat error:", err);
    }
  };

  const getStatusColor = () => {
    if (!panelDetail) return "#999";
    if (panelDetail.status === "available") return "#4CAF50";
    return "#FF9800";
  };

  return (
    <div style={{
      border: "1px solid var(--border)",
      borderRadius: "8px",
      padding: "15px",
      marginBottom: "15px",
      backgroundColor: "var(--bg-secondary)"
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h4 style={{ margin: "0 0 5px 0", color: getStatusColor(), fontWeight: "600" }}>
            {panelName}
          </h4>
          <p style={{ margin: "0", fontSize: "13px", color: "var(--text-secondary)" }}>
            {panelDetail ? panelDetail.description : "Model not yet built"}
          </p>
        </div>

        {panelDetail && panelDetail.status === "available" && (
          <button
            onClick={runAnalysis}
            disabled={analyzing}
            style={{
              padding: "8px 16px",
              backgroundColor: panelDetail.historical_result ? "#FF9800" : "#2196F3",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: analyzing ? "not-allowed" : "pointer"
            }}
          >
            {panelDetail.historical_result 
              ? "📋 View Historical Result" 
              : analyzing ? "Analyzing..." : "🔬 Analyze"}
          </button>
        )}

        {!panelDetail && (
          <span style={{
            padding: "8px 16px",
            backgroundColor: "#64748B",
            color: "white",
            borderRadius: "4px",
            fontSize: "12px",
            fontWeight: "500"
          }}>
            ⚠️ Not Available
          </span>
        )}
      </div>

      {panelDetail && (
        <div style={{ marginTop: "10px", fontSize: "12px" }}>
          <details>
            <summary style={{ cursor: "pointer", color: "var(--primary)", fontWeight: "500" }}>
              View detected inputs ({panelDetail.present_inputs.length})
            </summary>
            <ul style={{ marginTop: "5px", color: "var(--text-primary)" }}>
              {panelDetail.present_inputs.map(input => (
                <li key={input} style={{ color: "#059669", fontWeight: "500" }}>
                  ✓ {input}: {extractedData[input]}
                </li>
              ))}
              {panelDetail.missing_inputs.map(input => (
                <li key={input} style={{ color: "#D97706", fontWeight: "500" }}>
                  ⚠ {input}: Not found (optional)
                </li>
              ))}
            </ul>
          </details>
        </div>
      )}

      {result && (
        <div className="analysis-result-card">
          <h5>Analysis Result:</h5>
          <div className="result-item">
            <strong>Decision:</strong> <span className="result-value">{result.final_decision}</span>
          </div>
          <div className="result-item">
            <strong>Confidence:</strong> <span className="result-value">{(result.confidence * 100).toFixed(2)}%</span>
          </div>
          <div className="result-item">
            <strong>Source:</strong> <span className="result-value">{result.decision_source}</span>
          </div>
          
          <button
            onClick={() => setShowChat(!showChat)}
            className="btn-primary"
            style={{
              marginTop: "10px",
              padding: "6px 12px",
              backgroundColor: "#4CAF50",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer"
            }}
          >
            {showChat ? "Hide" : "Show"} AI Explanation 💬
          </button>

          {showChat && (
            <div style={{
              marginTop: "10px",
              padding: "10px",
              backgroundColor: "var(--bg-tertiary)",
              borderRadius: "4px",
              maxHeight: "300px",
              overflowY: "auto"
            }}>
              {chatMessages.length > 0 && (
                <div style={{
                  padding: "5px 10px",
                  backgroundColor: "rgba(8, 145, 178, 0.15)",
                  borderRadius: "4px",
                  marginBottom: "10px",
                  fontSize: "12px",
                  color: "#0E7490",
                  fontWeight: "600"
                }}>
                  💬 {chatMessages.length} message{chatMessages.length !== 1 ? 's' : ''} in this conversation
                </div>
              )}
              
              <div style={{ marginBottom: "10px" }}>
                {chatMessages.map((msg, idx) => (
                  <div
                    key={idx}
                    style={{
                      padding: "8px",
                      marginBottom: "5px",
                      backgroundColor: msg.role === "user" ? "rgba(8, 145, 178, 0.15)" : "rgba(245, 158, 11, 0.15)",
                      borderRadius: "4px",
                      fontSize: "13px",
                      color: "var(--text-primary)"
                    }}
                  >
                    <strong style={{ display: "block", marginBottom: "5px", color: "var(--text-primary)" }}>
                      {msg.role === "user" ? "You" : "AI Assistant"}:
                    </strong>
                    <div style={{ whiteSpace: "pre-wrap", lineHeight: "1.5", color: "var(--text-primary)" }}>
                      {msg.message}
                    </div>
                  </div>
                ))}
              </div>

              <div style={{ display: "flex", gap: "5px" }}>
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && sendChatMessage()}
                  placeholder="Ask about this result..."
                  style={{
                    flex: 1,
                    padding: "6px",
                    border: "1px solid var(--border)",
                    borderRadius: "4px",
                    backgroundColor: "var(--bg-primary)",
                    color: "var(--text-primary)"
                  }}
                />
                <button
                  onClick={sendChatMessage}
                  disabled={!chatInput.trim() || !sessionId}
                  style={{
                    padding: "6px 12px",
                    backgroundColor: !chatInput.trim() || !sessionId ? "#ccc" : "#2196F3",
                    color: "white",
                    border: "none",
                    borderRadius: "4px",
                    cursor: !chatInput.trim() || !sessionId ? "not-allowed" : "pointer"
                  }}
                >
                  Send
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default AnalyzerPanel;
