import React, { useState, useEffect } from "react";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";

const clientId = "38776683044-jfiipcpm08vs13u62o8mr046amjqeg4a.apps.googleusercontent.com"; // Replace with your actual Google Client ID

const GoogleAuth = () => {
  const [user, setUser] = useState(null);

  // Load user from localStorage on component mount
  useEffect(() => {
    const storedUser = localStorage.getItem("googleUser");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  // Handle login success
  const handleLoginSuccess = (credentialResponse) => {
    const jwtToken = credentialResponse.credential;

    // Decode JWT to get user info (basic decoding method)
    const userData = JSON.parse(atob(jwtToken.split(".")[1]));

    // Store user data in localStorage
    localStorage.setItem("googleUser", JSON.stringify(userData));

    // Update UI
    setUser(userData);
  };

  // Handle login failure
  const handleLoginFailure = () => {
    alert("Google login failed. Please try again.");
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem("googleUser");
    setUser(null);
  };

  return (
    <GoogleOAuthProvider clientId={clientId}>
      <div style={{ textAlign: "center", marginTop: "50px" }}>
        {user ? (
          <div>
            <h2>Welcome, {user.name}!</h2>
            <img
              src={user.picture}
              alt="User Profile"
              style={{ borderRadius: "50%", width: "100px", height: "100px" }}
            />
            <br />
            <button onClick={handleLogout}>Logout</button>
          </div>
        ) : (
          <GoogleLogin
            onSuccess={handleLoginSuccess}
            onError={handleLoginFailure}
          />
        )}
      </div>
    </GoogleOAuthProvider>
  );
};

export default GoogleAuth;
