import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "./NavigationBar.css";
import Logo from "../../assets/logo.png";

function NavigationBar() {
    const location = useLocation();
    const navigate = useNavigate();
    
    // Dummy authentication
    const isAuthenticated = localStorage.getItem("userToken"); 

    // Dummy authentication function to be replaced by google auth
    const handleAuth = () => {
        if (isAuthenticated) {
            localStorage.removeItem("userToken"); // Log out user
            navigate("/signin");
        } else {
            navigate("/signin");
        }
    };

    return (
        <div className="nav-bar">
            {/* Logo and Title */}
            <div className="nav-title">
                <div className="navBarLogo">
                    <img src={Logo} alt="Norman Police Department Logo" />
                </div>
                <Link to="/">CommsCheck</Link>
            </div>

            {/* Navigation Links */}
            <div className="nav-links">
                <Link to="/" className={location.pathname === "/" ? "active" : ""}>Home</Link>
                <Link to="/dispatchers" className={location.pathname === "/dispatchers" ? "active" : ""}>Dispatchers</Link>
                <Link to="/history" className={location.pathname === "/history" ? "active" : ""}>History</Link>

                {/* Sign In / Sign Out Button */}
                <div className="sign-in-button" onClick={handleAuth}>
                    {isAuthenticated ? "Sign Out" : "Sign In"}
                </div>
            </div>
        </div>
    );
}

export default NavigationBar;
