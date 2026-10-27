import React, { useState, useEffect } from 'react';
import { getOrderHistory } from '../services/api';

export default function OrdersHistory({ user, onOpenLogin }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [phoneSearch, setPhoneSearch] = useState(user?.phone || '');
  const [activeFilter, setActiveFilter] = useState('ALL');

  const fetchOrders = async (phone = '') => {
    try {
      setLoading(true);
      // If user is Admin, pass empty phone to fetch all orders
      const targetPhone = user?.role === 'ADMIN' ? '' : (phone || user?.phone || '');
      const data = await getOrderHistory(targetPhone);
      setOrders(data);
    } catch (err) {
      console.error('Error fetching order history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders(user?.phone || '');
  }, [user]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'DELIVERED':
        return { bg: '#dcfce7', text: '#15803d', border: '#86efac' };
      case 'OUT_FOR_DELIVERY':
        return { bg: '#f3e8ff', text: '#7e22ce', border: '#d8b4fe' };
      case 'PREPARING':
        return { bg: '#e0f2fe', text: '#0369a1', border: '#7dd3fc' };
      case 'CONFIRMED':
      case 'PLACED':
        return { bg: '#fef3c7', text: '#b45309', border: '#fde68a' };
      case 'CANCELLED':
        return { bg: '#fee2e2', text: '#b91c1c', border: '#fca5a5' };
      default:
        return { bg: '#f1f5f9', text: '#475569', border: '#cbd5e1' };
    }
  };

  const filteredOrders = activeFilter === 'ALL'
    ? orders
    : orders.filter((o) => o.status === activeFilter);

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '10px 0 40px' }}>
      {/* Title & Stats Header */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '16px',
        marginBottom: '24px',
        background: '#ffffff',
        padding: '20px 24px',
        borderRadius: '16px',
        boxShadow: '0 4px 20px rgba(0,0,0,0.04)'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '24px' }}>📜</span>
            <h2 style={{ margin: 0, fontSize: '22px', fontWeight: 800 }}>
              {user?.role === 'ADMIN' ? 'All Restaurant Orders (Admin View)' : 'Your Orders History'}
            </h2>
          </div>
          <p style={{ margin: '4px 0 0', fontSize: '13px', color: '#64748b' }}>
            {user?.role === 'ADMIN'
              ? 'Complete live log of delivery and dine-in orders across Spice Garden.'
              : user
                ? `Showing order history for ${user.name} (${user.phone || user.username})`
                : 'Sign in to automatically sync your previous food orders.'}
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          {!user && (
            <button
              onClick={onOpenLogin}
              style={{
                background: 'var(--color-primary)',
                color: '#fff',
                border: 'none',
                padding: '9px 16px',
                borderRadius: '8px',
                fontWeight: 700,
                fontSize: '13px',
                cursor: 'pointer'
              }}
            >
              🔐 Sign In
            </button>
          )}

          <button
            onClick={() => fetchOrders(phoneSearch)}
            style={{
              background: '#f1f5f9',
              color: '#334155',
              border: '1px solid #cbd5e1',
              padding: '9px 14px',
              borderRadius: '8px',
              fontWeight: 600,
              fontSize: '13px',
              cursor: 'pointer'
            }}
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Guest Phone Lookup (if not logged in) */}
      {!user && (
        <div style={{
          background: '#f8fafc',
          border: '1px dashed #cbd5e1',
          borderRadius: '12px',
          padding: '16px',
          marginBottom: '20px',
          display: 'flex',
          flexWrap: 'wrap',
          alignItems: 'center',
          gap: '12px'
        }}>
          <span style={{ fontSize: '13px', fontWeight: 600, color: '#475569' }}>
            Look up orders by phone:
          </span>
          <input
            type="tel"
            placeholder="Enter 10-digit phone"
            value={phoneSearch}
            onChange={(e) => setPhoneSearch(e.target.value)}
            style={{
              padding: '7px 12px',
              borderRadius: '8px',
              border: '1px solid #cbd5e1',
              fontSize: '13px',
              flex: '1',
              minWidth: '180px'
            }}
          />
          <button
            onClick={() => fetchOrders(phoneSearch)}
            style={{
              background: '#334155',
              color: '#fff',
              border: 'none',
              padding: '7px 16px',
              borderRadius: '8px',
              fontSize: '13px',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            Find Orders
          </button>
        </div>
      )}

      {/* Status Filter Chips */}
      <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', marginBottom: '20px', paddingBottom: '4px' }}>
        {['ALL', 'PLACED', 'PREPARING', 'OUT_FOR_DELIVERY', 'DELIVERED'].map((st) => (
          <button
            key={st}
            onClick={() => setActiveFilter(st)}
            style={{
              padding: '6px 14px',
              borderRadius: '20px',
              border: '1px solid',
              borderColor: activeFilter === st ? 'var(--color-primary)' : '#e2e8f0',
              background: activeFilter === st ? 'var(--color-primary)' : '#ffffff',
              color: activeFilter === st ? '#ffffff' : '#64748b',
              fontSize: '12px',
              fontWeight: 700,
              cursor: 'pointer',
              whiteSpace: 'nowrap'
            }}
          >
            {st.replace(/_/g, ' ')}
          </button>
        ))}
      </div>

      {/* Orders List */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '50px 20px', color: '#94a3b8' }}>
          <div style={{ fontSize: '32px', marginBottom: '8px' }}>🍲</div>
          <p>Fetching your orders from MySQL database...</p>
        </div>
      ) : filteredOrders.length === 0 ? (
        <div style={{
          textAlign: 'center',
          padding: '60px 20px',
          background: '#ffffff',
          borderRadius: '16px',
          boxShadow: '0 4px 14px rgba(0,0,0,0.03)'
        }}>
          <div style={{ fontSize: '40px', marginBottom: '12px' }}>📦</div>
          <h3 style={{ fontSize: '18px', fontWeight: 700, margin: '0 0 6px', color: '#1e293b' }}>
            No Orders Found
          </h3>
          <p style={{ fontSize: '13px', color: '#64748b', maxWidth: '380px', margin: '0 auto 16px' }}>
            You haven't placed any orders yet, or no orders match the selected filter.
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {filteredOrders.map((ord) => {
            const stColor = getStatusColor(ord.status);
            return (
              <div
                key={ord.id}
                style={{
                  background: '#ffffff',
                  borderRadius: '16px',
                  padding: '20px 22px',
                  boxShadow: '0 4px 16px rgba(0,0,0,0.04)',
                  border: '1px solid #f1f5f9',
                  transition: 'transform 0.15s ease'
                }}
              >
                {/* Order Top Bar */}
                <div style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: '10px',
                  borderBottom: '1px solid #f1f5f9',
                  paddingBottom: '12px',
                  marginBottom: '14px'
                }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '16px', fontWeight: 800, color: '#0f172a' }}>
                        {ord.order_number}
                      </span>
                      <span style={{
                        fontSize: '11px',
                        fontWeight: 700,
                        padding: '3px 8px',
                        borderRadius: '6px',
                        background: '#f8fafc',
                        border: '1px solid #e2e8f0',
                        color: '#475569'
                      }}>
                        {ord.order_type === 'DELIVERY' ? '🛵 Home Delivery' : '🪑 Dine-in'}
                      </span>
                    </div>
                    <span style={{ fontSize: '12px', color: '#94a3b8' }}>
                      📅 {ord.created_at}
                    </span>
                  </div>

                  {/* Status Badge */}
                  <span style={{
                    fontSize: '12px',
                    fontWeight: 800,
                    padding: '4px 12px',
                    borderRadius: '20px',
                    background: stColor.bg,
                    color: stColor.text,
                    border: `1px solid ${stColor.border}`
                  }}>
                    ● {ord.status.replace(/_/g, ' ')}
                  </span>
                </div>

                {/* Items List */}
                <div style={{ marginBottom: '14px' }}>
                  <div style={{ fontSize: '12px', fontWeight: 700, color: '#64748b', marginBottom: '8px' }}>
                    ORDERED ITEMS:
                  </div>
                  {ord.items && ord.items.length > 0 ? (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                      {ord.items.map((it, idx) => (
                        <div
                          key={idx}
                          style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            fontSize: '13px',
                            color: '#1e293b'
                          }}
                        >
                          <span>
                            <strong style={{ color: 'var(--color-primary)' }}>{it.quantity}×</strong> {it.name}
                          </span>
                          <span style={{ fontWeight: 600 }}>₹{it.total_price.toFixed(2)}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div style={{ fontSize: '13px', color: '#94a3b8', fontStyle: 'italic' }}>
                      Standard Chef Combo / Placed via Cart
                    </div>
                  )}
                </div>

                {/* Delivery Address & Payment */}
                <div style={{
                  background: '#f8fafc',
                  borderRadius: '10px',
                  padding: '10px 14px',
                  marginBottom: '14px',
                  fontSize: '12px',
                  color: '#475569',
                  display: 'flex',
                  flexWrap: 'wrap',
                  justifyContent: 'space-between',
                  gap: '8px'
                }}>
                  <div>
                    <strong>📍 Address:</strong> {ord.delivery_address}
                  </div>
                  <div>
                    <strong>💳 Payment:</strong> {ord.payment_status}
                  </div>
                </div>

                {/* Price Breakdown Footer */}
                <div style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  borderTop: '1px solid #f1f5f9',
                  paddingTop: '12px',
                  gap: '10px'
                }}>
                  <div style={{ fontSize: '12px', color: '#64748b', display: 'flex', gap: '14px' }}>
                    <span>Subtotal: ₹{ord.subtotal.toFixed(2)}</span>
                    <span>GST (5%): ₹{ord.tax.toFixed(2)}</span>
                    <span>Delivery: {ord.delivery_fee === 0 ? 'FREE' : `₹${ord.delivery_fee.toFixed(2)}`}</span>
                  </div>

                  <div style={{ fontSize: '16px', fontWeight: 900, color: '#0f172a' }}>
                    Total: <span style={{ color: 'var(--color-primary)' }}>₹{ord.total_amount.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
