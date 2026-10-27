import React, { useState } from 'react';
import { getOrders } from '../services/api';

const ORDER_STEPS = ['PLACED', 'PREPARING', 'READY', 'OUT_FOR_DELIVERY', 'DELIVERED'];

export default function OrderTracking() {
  const [orderQuery, setOrderQuery] = useState('');
  const [orderData, setOrderData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleTrack = async (e) => {
    if (e) e.preventDefault();
    const cleanNum = orderQuery.trim().toUpperCase();
    if (!cleanNum) {
      setError('Please enter your order number (e.g. ORD-1234ABCD)');
      return;
    }

    setLoading(true);
    setError(null);
    setOrderData(null);

    try {
      const orders = await getOrders(1);
      const found = orders.find((o) => o.order_number === cleanNum);

      if (found) {
        setOrderData(found);
      } else {
        setError(`Order "${cleanNum}" was not found in our system. Please check your order number.`);
      }
    } catch (err) {
      setError('Could not connect to orders service. Please make sure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const getStepStatus = (stepName) => {
    if (!orderData) return '';
    const currentIndex = ORDER_STEPS.indexOf(orderData.status);
    const stepIndex = ORDER_STEPS.indexOf(stepName);

    if (stepIndex < currentIndex) return 'done';
    if (stepIndex === currentIndex) return 'active';
    return '';
  };

  return (
    <div className="tracking-wrap">
      <div className="section-header">
        <h2>📦 Live Order Tracking</h2>
        <p>Track your food delivery in real-time or ask our AI Agent at the bottom right!</p>
      </div>

      <form onSubmit={handleTrack} className="tracking-search-bar">
        <input
          type="text"
          placeholder="Enter your Order ID (e.g. ORD-A1B2C3D4)"
          value={orderQuery}
          onChange={(e) => setOrderQuery(e.target.value)}
        />
        <button type="submit" className="submit-btn" style={{ padding: '0 24px' }} disabled={loading}>
          {loading ? 'Tracking...' : 'Track'}
        </button>
      </form>

      {error && (
        <div style={{ color: '#c62828', textAlign: 'center', background: '#ffebee', padding: '12px', borderRadius: '8px' }}>
          {error}
        </div>
      )}

      {orderData && (
        <div style={{ background: '#fff', borderRadius: '14px', padding: '24px', boxShadow: '0 4px 16px rgba(0,0,0,0.06)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #edf2f7', paddingBottom: '12px' }}>
            <div>
              <span style={{ fontSize: '12px', color: '#718096', textTransform: 'uppercase', fontWeight: 'bold' }}>Order Number</span>
              <h3 style={{ margin: 0, color: '#e65100' }}>{orderData.order_number}</h3>
            </div>
            <div style={{ textAlign: 'right' }}>
              <span style={{ fontSize: '12px', color: '#718096' }}>Total Amount</span>
              <h3 style={{ margin: 0 }}>₹{orderData.total_amount}</h3>
            </div>
          </div>

          {/* Stepper Progress Bar */}
          <div className="stepper">
            <div className={`step ${getStepStatus('PLACED')}`}>
              <div className="step-circle">1</div>
              <span className="step-title">Placed</span>
            </div>
            <div className={`step ${getStepStatus('PREPARING')}`}>
              <div className="step-circle">2</div>
              <span className="step-title">Kitchen</span>
            </div>
            <div className={`step ${getStepStatus('READY')}`}>
              <div className="step-circle">3</div>
              <span className="step-title">Ready</span>
            </div>
            <div className={`step ${getStepStatus('OUT_FOR_DELIVERY')}`}>
              <div className="step-circle">4</div>
              <span className="step-title">On Way</span>
            </div>
            <div className={`step ${getStepStatus('DELIVERED')}`}>
              <div className="step-circle">5</div>
              <span className="step-title">Delivered</span>
            </div>
          </div>

          <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '8px', fontSize: '13px' }}>
            <p><strong>Current Status:</strong> <span style={{ color: '#e65100', fontWeight: 'bold' }}>{orderData.status}</span></p>
            <p><strong>Order Type:</strong> {orderData.order_type}</p>
            <p><strong>Payment Status:</strong> <span style={{ color: '#2e7d32', fontWeight: 'bold' }}>{orderData.payment_status}</span></p>
          </div>
        </div>
      )}
    </div>
  );
}
