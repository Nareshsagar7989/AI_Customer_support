import React, { useState } from 'react';
import { bookTable } from '../services/api';

export default function DineInReservation({ user, onRequireLogin }) {
  const [formData, setFormData] = useState({
    customer_name: user?.name || user?.username || '',
    phone: user?.phone || '',
    restaurant_id: 1,
    reservation_date: new Date().toISOString().split('T')[0],
    start_time: '19:30:00',
    party_size: 2,
    special_request: ''
  });

  const [loading, setLoading] = useState(false);
  const [confirmedBooking, setConfirmedBooking] = useState(null);
  const [error, setError] = useState(null);

  React.useEffect(() => {
    if (user) {
      setFormData((prev) => ({
        ...prev,
        customer_name: user.name || user.username || prev.customer_name,
        phone: user.phone || prev.phone
      }));
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if user is signed in
    if (!user) {
      if (onRequireLogin) {
        onRequireLogin('Please sign in to book your dining table!');
      }
      return;
    }

    if (!formData.customer_name.trim() || !formData.phone.trim()) {
      setError('Please provide your name and phone number.');
      return;
    }

    setLoading(true);
    setError(null);
    setConfirmedBooking(null);

    try {
      const res = await bookTable(formData);
      setConfirmedBooking(res);
    } catch (err) {
      setError('Failed to book table. Please make sure backend is reachable.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="reservation-card">
      <div className="section-header">
        <h2>🪑 Dine-in Table Reservation</h2>
        <p>Book your premium dining table online or ask our AI Concierge at the bottom right!</p>
      </div>

      {!user && (
        <div style={{
          background: 'rgba(255, 109, 0, 0.08)',
          border: '1px solid rgba(255, 109, 0, 0.3)',
          borderRadius: '10px',
          padding: '12px 16px',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '12px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '20px' }}>🔒</span>
            <span style={{ fontSize: '13.5px', color: '#334155' }}>
              <strong>Authentication Required:</strong> Please sign in to reserve your table.
            </span>
          </div>
          <button
            type="button"
            className="toast-action-btn"
            style={{ padding: '6px 14px', fontSize: '12.5px' }}
            onClick={() => onRequireLogin && onRequireLogin('Please sign in to book your dining table!')}
          >
            Sign In Now
          </button>
        </div>
      )}

      <form onSubmit={handleSubmit} className="form-grid">
        <div className="form-group">
          <label>Your Name</label>
          <input
            type="text"
            required
            placeholder="e.g. Rahul Sharma"
            value={formData.customer_name}
            onChange={(e) => setFormData({ ...formData, customer_name: e.target.value })}
          />
        </div>

        <div className="form-group">
          <label>Phone Number</label>
          <input
            type="tel"
            required
            placeholder="e.g. 9876543210"
            value={formData.phone}
            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
          />
        </div>

        <div className="form-group">
          <label>Reservation Date</label>
          <input
            type="date"
            required
            value={formData.reservation_date}
            min={new Date().toISOString().split('T')[0]}
            onChange={(e) => setFormData({ ...formData, reservation_date: e.target.value })}
          />
        </div>

        <div className="form-group">
          <label>Time Slot</label>
          <select
            value={formData.start_time}
            onChange={(e) => setFormData({ ...formData, start_time: e.target.value })}
          >
            <option value="12:30:00">12:30 PM (Lunch)</option>
            <option value="13:30:00">01:30 PM (Lunch)</option>
            <option value="19:00:00">07:00 PM (Dinner)</option>
            <option value="19:30:00">07:30 PM (Dinner)</option>
            <option value="20:00:00">08:00 PM (Dinner)</option>
            <option value="20:30:00">08:30 PM (Dinner)</option>
            <option value="21:00:00">09:00 PM (Dinner)</option>
          </select>
        </div>

        <div className="form-group">
          <label>Number of Guests</label>
          <select
            value={formData.party_size}
            onChange={(e) => setFormData({ ...formData, party_size: parseInt(e.target.value, 10) })}
          >
            {[1, 2, 3, 4, 5, 6, 8, 10, 12].map((num) => (
              <option key={num} value={num}>{num} {num === 1 ? 'Guest' : 'Guests'}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Seating Preference</label>
          <select
            onChange={(e) => setFormData({ ...formData, special_request: e.target.value })}
            value={formData.special_request}
          >
            <option value="">Standard Seating</option>
            <option value="Window table with calm atmosphere">Window Table</option>
            <option value="Open-air rooftop seating">Open-Air Rooftop</option>
            <option value="Air-conditioned central hall">Indoor AC Hall</option>
            <option value="Private celebration / Birthday">Birthday / Anniversary Decor</option>
          </select>
        </div>

        <div className="form-group full-width">
          <label>Special Requests (Optional)</label>
          <textarea
            rows="2"
            placeholder="High chair for baby, dietary allergy, birthday celebration, etc."
            value={formData.special_request}
            onChange={(e) => setFormData({ ...formData, special_request: e.target.value })}
          />
        </div>

        <button type="submit" className="submit-btn" style={{ gridColumn: 'span 2' }} disabled={loading}>
          {loading ? 'Confirming Reservation with Restaurant...' : 'Reserve Table Now ✨'}
        </button>
      </form>

      {error && (
        <div style={{ color: '#c62828', marginTop: '16px', textAlign: 'center', fontWeight: 'bold' }}>
          {error}
        </div>
      )}

      {/* Confirmed Ticket Card */}
      {confirmedBooking && (
        <div className="ticket-card">
          <div className="ticket-header">
            <div>
              <h4 style={{ margin: 0, color: '#a5d6a7' }}>🎉 Table Reserved Successfully!</h4>
              <small style={{ color: '#cfd8dc' }}>Spice Garden, Madhapur, Hyderabad</small>
            </div>
            <div className="ticket-code">{confirmedBooking.confirmation_code}</div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '13.5px' }}>
            <p>📅 <strong>Date:</strong> {confirmedBooking.reservation_date}</p>
            <p>⏰ <strong>Time:</strong> {confirmedBooking.start_time}</p>
            <p>👥 <strong>Guests:</strong> {confirmedBooking.party_size} People</p>
            <p>✨ <strong>Status:</strong> <span style={{ color: '#69f0ae', fontWeight: 'bold' }}>{confirmedBooking.status}</span></p>
          </div>
          <p style={{ marginTop: '10px', fontSize: '12px', color: '#b0bec5', fontStyle: 'italic' }}>
            Note: Your table will be held for 15 minutes past booking time. Enjoy complimentary valet parking!
          </p>
        </div>
      )}
    </div>
  );
}
