import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Sidebar from "../../components/SideBar/SideBar";
import Results from "../ResultsPage/ResultsPage";
import "./HistoryPage.css";

export default function History() {
  // Mock session data
  const [sessions] = useState([
    {
      session: "1289",
      transcript: "User: Hello I need help with \n Dispatcher: Hi there! I'd be happy to",
      summary: {
        requiredQuestions: ["Identification", "Issue description", "Contact details", "Verify solution"],
        completenessScore: 75,
      },
    },
    {
      session: "1290",
      transcript: "User: I have an issue \n Dispatcher: Can you describe the issue?",
      summary: {
        requiredQuestions: ["Identification", "Issue description", "Contact details"],
        completenessScore: 60,
      },
    },
  ]);

  return (
    <div className="history-container">
      <Sidebar sessions={sessions} /> {/* Pass session data to Sidebar */}

      {/* Route to handle session selection */}
      <div className="history-content">
        <Routes>
          <Route path="/" element={<p>Select a session from the sidebar.</p>} />
          <Route path=":sessionId" element={<Results sessions={sessions} />} />
        </Routes>
      </div>
    </div>
  );
}
