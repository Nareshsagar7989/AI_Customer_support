import React, { useState } from 'react';
import { registerUser } from '../services/api';

export default function RegisterPage({ 
  onRegisterSuccess, 
  onNavigateLogin, 
  onBackToHome 
}) {
  const [username, setUsername] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const regUsername = username.trim();
      await registerUser({ username: regUsername, password, name, phone, email });
      
      // Immediately redirect to LoginPage with pre-filled username
      onRegisterSuccess(regUsername);
    } catch (err) {
      setError(err.message || 'Registration failed. Please try a different username.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page-wrapper">
      {/* Top Bar with Brand and Back Navigation */}
      <div className="auth-page-topbar">
        <button className="auth-back-btn" onClick={onBackToHome}>
          <span>←</span> Back to Restaurant
        </button>
        <div className="auth-topbar-brand" onClick={onBackToHome}>
          <span>🌶️</span>
          <strong>Spice Garden</strong>
        </div>
      </div>

      <div className="auth-page-card-container">
        <div className="auth-page-card">
          {/* Card Header */}
          <div className="auth-card-header">
            <div className="auth-card-icon-pill register">
              <span>📝</span>
            </div>
            <h2>Create Customer Account</h2>
            <p>Join Spice Garden to order Hyderabadi delicacies, reserve tables, and chat with AI.</p>
          </div>

          {/* Error Notification */}
          {error && (
            <div className="auth-alert error">
              ⚠️ {error}
            </div>
          )}

          {/* Registration Form */}
          <form onSubmit={handleRegister} className="auth-form">
            <div className="form-group">
              <label>Username *</label>
              <input
                type="text"
                required
                placeholder="Choose a unique username (e.g. naresh_s)"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Full Name *</label>
              <input
                type="text"
                required
                placeholder="Your full name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Phone Number * (for delivery & order tracking)</label>
              <input
                type="tel"
                required
                placeholder="10-digit mobile number"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Password *</label>
              <input
                type="password"
                required
                placeholder="Create a secure password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <span className="form-helper">
                Passwords are automatically hashed into 64-character SHA-256 string.
              </span>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="submit-btn"
              style={{ width: '100%', marginTop: '8px', padding: '13px', fontSize: '15px' }}
            >
              {loading ? 'Creating Account...' : 'Register as Customer ✨'}
            </button>

            <div className="auth-switch-prompt">
              <span>Already have an account?</span>
              <button
                type="button"
                className="auth-link-btn"
                onClick={onNavigateLogin}
              >
                Sign In to Account 👈
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
