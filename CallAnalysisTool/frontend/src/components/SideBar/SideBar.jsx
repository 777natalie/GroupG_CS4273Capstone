import React from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css';

function Sidebar({ sessions = [] }) {
    return (
        <div className="sidebar">
            {sessions.length > 0 && (
                <>
                <h3>Sessions</h3>
                {/* Loop through session and display in sidebar */}
                <ul className="session-list">
                    {sessions.map((session, index) => (
                    <li key={index}>
                        {/* Link to the results page for this session */}
                        <Link to={`/history/${session.session}`}>Session #{session.session}</Link>
                    </li>
                    ))}
                </ul>
                </>
            )}
        </div>
    );
}

export default Sidebar;
