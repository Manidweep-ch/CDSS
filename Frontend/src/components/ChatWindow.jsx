import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";

function ChatWindow({ evaluationId }) {
  const [sessions, setSessions] = useState([]);
  const [activeSession, setActiveSession] = useState(null);
  const [message, setMessage] = useState("");

  const loadSessions = async () => {
    const response = await axiosClient.get(`/chat/${evaluationId}`);
    setSessions(response.data);
  };

  useEffect(() => {
    if (evaluationId) {
      loadSessions();
    }
  }, [evaluationId]);

  const startGlobalChat = async () => {
    const response = await axiosClient.post("/chat/start", null, {
      params: {
        evaluation_id: evaluationId,
        session_type: "global",
      },
    });

    setActiveSession(response.data.session_id);
    loadSessions();
  };

  const sendMessage = async () => {
    if (!message) return;

    await axiosClient.post("/chat/message", null, {
      params: {
        session_id: activeSession,
        message: message,
      },
    });

    setMessage("");
    loadSessions();
  };

  return (
    <div style={{ marginTop: "30px", borderTop: "1px solid gray", paddingTop: "10px" }}>
      <h3>Explainability Chat</h3>

      {!activeSession && (
        <button onClick={startGlobalChat}>
          Start Global Chat
        </button>
      )}

      {sessions.map((session) => (
        <div key={session.session_id}>
          <h4>{session.session_type} Session</h4>

          {session.messages.map((msg, index) => (
            <p key={index}>
              <b>{msg.role}:</b> {msg.message}
            </p>
          ))}
        </div>
      ))}

      {activeSession && (
        <>
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask about this evaluation..."
          />
          <button onClick={sendMessage} style={{ marginLeft: "5px" }}>
            Send
          </button>
        </>
      )}
    </div>
  );
}

export default ChatWindow;