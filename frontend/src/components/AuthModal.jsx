import React, { useState, useEffect } from 'react';
import { loginUser, registerUser } from '../services/api';

export default function AuthModal({ isOpen, onClose, onLoginSuccess, initialTab = 'login' }) {
  const [tab, setTab] = useState(initialTab); // 'login' | 'register'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  // Form states
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    if (isOpen) {
      setTab(initialTab);
      setError('');
      setSuccessMsg('');
    }
  }, [isOpen, initialTab]);

  if (!isOpen) return null;

  const handleQuickLogin = async (usr, pwd) => {
    setError('');
    setSuccessMsg('');
    setLoading(true);
    setTab('login');
    setUsername(usr);
    setPassword(pwd);

    try {
      const data = await loginUser({ username: usr, password: pwd });
      setSuccessMsg(`Welcome, ${data.name || data.username}! (${data.role})`);
      setTimeout(() => {
        onLoginSuccess(data);
        onClose();
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
        onClose();
      }, 600);
    } catch (err) {
      setError(err.message || 'Login failed. Please check credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMsg('');
    setLoading(true);

    try {
      const registeredUsername = username.trim();
      await registerUser({ username: registeredUsername, password, name, phone, email });
      
      // Immediately switch to login page with pre-filled username
      setTab('login');
      setUsername(registeredUsername);
      setPassword('');
      setSuccessMsg(`✅ Account created for "${registeredUsername}"! Please sign in below.`);
    } catch (err) {
      setError(err.message || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose} style={{ zIndex: 1100 }}>
      <div 
        className="modal-card auth-modal-premium" 
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: '460px', width: '92%' }}
      >
        {/* Header */}
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ fontSize: '26px' }}>{tab === 'login' ? '🔐' : '📝'}</span>
            <div>
              <h3 style={{ margin: 0, fontSize: '19px', fontWeight: 800, color: '#0f172a' }}>
                {tab === 'login' ? 'Sign In to Your Account' : 'Create New Account'}
              </h3>
              <p style={{ margin: '2px 0 0', fontSize: '12.5px', color: '#64748b' }}>
                {tab === 'login' 
                  ? 'Access food ordering, table bookings & AI assistant' 
                  : 'Join to order food & track order history in real-time'}
              </p>
            </div>
          </div>
          <button className="modal-close-btn" onClick={onClose} title="Close">✕</button>
        </div>

        {/* Dedicated Tab Switchers */}
        <div className="auth-tab-capsule">
          <button
            type="button"
            className={`auth-tab-btn ${tab === 'login' ? 'active' : ''}`}
            onClick={() => { setTab('login'); setError(''); setSuccessMsg(''); }}
          >
            <span>🔑</span> Sign In
          </button>
          <button
            type="button"
            className={`auth-tab-btn ${tab === 'register' ? 'active' : ''}`}
            onClick={() => { setTab('register'); setError(''); setSuccessMsg(''); }}
          >
            <span>📝</span> Register (New User)
          </button>
        </div>

        {/* 1-Click "Continue as..." Hardcoded Recruiter Demo Access */}
        {tab === 'login' && (
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
        )}

        {/* Notifications */}
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

        {/* Sign In View */}
        {tab === 'login' ? (
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
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <span className="form-helper">
                Stored in DB with 64-character SHA-256 secure hash.
              </span>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="submit-btn"
              style={{ width: '100%', marginTop: '6px', padding: '12px' }}
            >
              {loading ? 'Authenticating...' : 'Sign In 🚀'}
            </button>

            <div className="auth-switch-prompt">
              <span>Don't have an account yet?</span>
              <button
                type="button"
                className="auth-link-btn"
                onClick={() => { setTab('register'); setError(''); setSuccessMsg(''); }}
              >
                Register as Customer 👉
              </button>
            </div>
          </form>
        ) : (
          /* Register View */
          <form onSubmit={handleRegister} className="auth-form">
            <div className="form-group">
              <label>Username *</label>
              <input
                type="text"
                required
                placeholder="Choose unique username (e.g. naresh_s)"
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
              <label>Phone Number (for Order Delivery & Tracking) *</label>
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
                placeholder="Create password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <span className="form-helper">
                Encrypted into 64-character SHA-256 hash before storing in database.
              </span>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="submit-btn"
              style={{ width: '100%', marginTop: '6px', padding: '12px' }}
            >
              {loading ? 'Creating Account...' : 'Create Account & Continue ✨'}
            </button>

            <div className="auth-switch-prompt">
              <span>Already registered?</span>
              <button
                type="button"
                className="auth-link-btn"
                onClick={() => { setTab('login'); setError(''); setSuccessMsg(''); }}
              >
                Sign In to Account 👈
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
