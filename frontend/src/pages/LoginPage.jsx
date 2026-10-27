import React, { useState } from 'react';
import { loginUser } from '../services/api';

export default function LoginPage({ 
  onLoginSuccess, 
  onNavigateRegister, 
  onBackToHome,
  prefilledUsername = '',
  initialSuccessMsg = ''
}) {
  const [username, setUsername] = useState(prefilledUsername);
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState(initialSuccessMsg);

  const handleQuickLogin = async (usr, pwd) => {
    setError('');
    setSuccessMsg('');
    setLoading(true);
    setUsername(usr);
    setPassword(pwd);

    try {
      const data = await loginUser({ username: usr, password: pwd });
      setSuccessMsg(`Welcome, ${data.name || data.username}! (${data.role})`);
      setTimeout(() => {
        onLoginSuccess(data);
      }, 500);
    } catch (err) {
      setError(err.message || 'Login failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMsg('');
    setLoading(true);

    try {
      const data = await loginUser({ username: username.trim(), password });
      setSuccessMsg(`Welcome back, ${data.name || data.username}! (${data.role})`);
      setTimeout(() => {
        onLoginSuccess(data);
      }, 600);
    } catch (err) {
      setError(err.message || 'Login failed. Please check credentials.');
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
            <div className="auth-card-icon-pill">
              <span>🔑</span>
            </div>
            <h2>Sign In to Spice Garden</h2>
            <p>Access autonomous AI ordering, live order tracking, and table reservations.</p>
          </div>

          {/* 1-Click "Continue as..." Hardcoded Recruiter Demo Access */}
          <div className="recruiter-quick-access">
            <div className="quick-access-title">
              <span>⚡ CONTINUE AS (1-CLICK RECRUITER DEMO)</span>
              <span className="quick-access-tag">Instant Access</span>
            </div>

            <div className="continue-as-grid">
              <button
                type="button"
                disabled={loading}
                onClick={() => handleQuickLogin('ADMIN370', 'Admin@370')}
                className="continue-as-btn admin"
              >
                <div className="continue-as-header">
                  <span className="continue-icon">👑</span>
                  <div className="continue-label">Continue as Admin</div>
                </div>
                <div className="continue-creds">
                  <div><strong>User:</strong> <code>ADMIN370</code></div>
                  <div><strong>Pass:</strong> <code>Admin@370</code></div>
                </div>
                <div className="continue-hint">Full Admin Portal Access →</div>
              </button>

              <button
                type="button"
                disabled={loading}
                onClick={() => handleQuickLogin('customer_demo', 'Customer@123')}
                className="continue-as-btn customer"
              >
                <div className="continue-as-header">
                  <span className="continue-icon">👤</span>
                  <div className="continue-label">Continue as Customer</div>
                </div>
                <div className="continue-creds">
                  <div><strong>User:</strong> <code>customer_demo</code></div>
                  <div><strong>Pass:</strong> <code>Customer@123</code></div>
                </div>
                <div className="continue-hint">Orders & Booking Access →</div>
              </button>
            </div>
          </div>

          {/* Error / Success Notifications */}
          {error && (
            <div className="auth-alert error">
              ⚠️ {error}
            </div>
          )}
          {successMsg && (
            <div className="auth-alert success">
              {successMsg}
            </div>
          )}

          {/* Sign In Form */}
          <form onSubmit={handleLogin} className="auth-form">
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                required
                placeholder="Enter username (e.g. ADMIN370 or customer_demo)"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                required
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <span className="form-helper">
                Passwords are encrypted using 64-character SHA-256 hash.
              </span>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="submit-btn"
              style={{ width: '100%', marginTop: '8px', padding: '13px', fontSize: '15px' }}
            >
              {loading ? 'Signing In...' : 'Sign In 🚀'}
            </button>

            <div className="auth-switch-prompt">
              <span>Don't have an account yet?</span>
              <button
                type="button"
                className="auth-link-btn"
                onClick={onNavigateRegister}
              >
                Register as New Customer 👉
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
