import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import "./SignInPage.css";
import GoogleAuth from './GoogleAuth.jsx'; // Adjust the path based on the file structure


const clientId = "38776683044-jfiipcpm08vs13u62o8mr046amjqeg4a.apps.googleusercontent.com";

export default function SignIn() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Dummy email/password login handler
  const handleSignIn = (e) => {
    e.preventDefault();
    if (email === "user@example.com" && password === "password") {
      navigate("/dashboard");
    } else {
      setError("Invalid email or password.");
    }
  };

  // Handle Google login success
  const handleGoogleSuccess = (credentialResponse) => {
    const jwtToken = credentialResponse.credential;
    const userData = JSON.parse(atob(jwtToken.split(".")[1]));

    // Save user and navigate
    localStorage.setItem("googleUser", JSON.stringify(userData));
    navigate("/dashboard");
  };

  // Handle Google login failure
  const handleGoogleFailure = () => {
    setError("Google login failed. Please try again.");
  };

  return (
    <div className="signin-container">
      <div className="signin-box">
        <h1>Sign In</h1>
        {error && <p className="error-message">{error}</p>}

        <form onSubmit={handleSignIn}>
          <div className="input-group">
            <label>Email</label>
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="options">
            <label>
              <input type="checkbox" /> Remember Me
            </label>
            <a href="/forgot-password">Forgot Password?</a>
          </div>
          <button type="submit" className="signin-button">Sign In</button>
        </form>


        {/* Google OAuth Login */}
        <GoogleOAuthProvider clientId={clientId}>
          <div className="google-login-wrapper">
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={handleGoogleFailure}
            />
          </div>
        </GoogleOAuthProvider>

        <p className="signup-text">
          Don't have an account? <a href="/signup">Sign Up</a>
        </p>
      </div>
    </div>
  );
}
