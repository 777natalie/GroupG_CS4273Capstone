import React, { useState } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import "./DispatchersPage.css";

const dispatchers = [
  { id: 1, name: "John Doe", score: 85, history: ["1289", "1290"] },
  { id: 2, name: "Jane Smith", score: 92, history: ["1291", "1292"] },
  { id: 3, name: "Emily Johnson", score: 78, history: ["1293"] },
  { id: 4, name: "Michael Brown", score: 88, history: ["1294", "1295"] },
];

export default function DispatcherPage() {
  const [search, setSearch] = useState("");
  const [selectedDispatcher, setSelectedDispatcher] = useState(null);

  const filteredDispatchers = dispatchers.filter((dispatcher) =>
    dispatcher.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="container">
      <div className="search-section">
        <input
          type="text"
          placeholder="Search dispatcher..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-input"
        />
        {search && (
          <div className="search-results">
            {filteredDispatchers.map((dispatcher) => (
              <div
                key={dispatcher.id}
                className="search-item"
                onClick={() => {
                  setSelectedDispatcher(dispatcher);
                  setSearch("");
                }}
              >
                {dispatcher.name}
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="profile-section">
        {selectedDispatcher && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="card">
              <div className="card-content">
                <h2 className="card-title">{selectedDispatcher.name}</h2>
                <p className="card-score">
                  Overall Score: {selectedDispatcher.score}%
                </p>
                <h3 className="card-history-title">Transcript History</h3>
                <ul className="card-history-list">
                  {selectedDispatcher.history.map((sessionId) => (
                    <li key={sessionId}>
                      <Link
                        to={`/history/${sessionId}`}
                        className="card-link"
                      >
                        Session {sessionId}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
