import React from "react";
import { useParams, useLocation } from "react-router-dom";
import TranscriptSection from "../../components/TranscriptDisplaySectionComponent";
import SummarySection from "../../components/SummaryDisplaySectionComponent";
import AdditionalDetailsSection from "../../components/AdditionalDetailSectionComponent";

export default function ResultsPage({ sessions }) {
  const { sessionId } = useParams();
  const location = useLocation();
  const resultsData = location.state;

  // Find the selected session data (if you are still using the sessions prop)
  const session = sessions ? sessions.find((s) => s.session === sessionId) : null;

  if (sessions && !session) {
    return <h2>Session not found</h2>;
  }

  const natureCode = resultsData?.response?.nature_code;
  const requiredQuestions = resultsData?.response?.required_questions;

  return (
    <div className="results-container">
      {/* Pass natureCode and requiredQuestions as props */}
      <SummarySection natureCode={natureCode} requiredQuestions={requiredQuestions} />
    </div>
  );
}