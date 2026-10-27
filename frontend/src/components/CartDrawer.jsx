import React, { useState } from 'react';
import { createOrder } from '../services/api';

export default function CartDrawer({ 
  isOpen, 
  onClose, 
  cart, 
  onClearCart, 
  onIncreaseQty, 
  onDecreaseQty,
  user,
  onRequireLogin
}) {
  const [loading, setLoading] = useState(false);
  const [placedOrder, setPlacedOrder] = useState(null);
  const [error, setError] = useState(null);
  const [deliveryAddress, setDeliveryAddress] = useState('');
  const [customerPhone, setCustomerPhone] = useState(user?.phone || '');

  React.useEffect(() => {
    if (user?.phone && !customerPhone) {
      setCustomerPhone(user.phone);
    }
  }, [user]);

  if (!isOpen) return null;

  const subtotal = cart.reduce((acc, item) => acc + item.price * item.quantity, 0);
  const tax = Math.round(subtotal * 0.05); // 5% GST
  const deliveryFee = subtotal > 500 ? 0 : 40;
  const grandTotal = subtotal + tax + deliveryFee;

  const handleCheckout = async () => {
    if (!user) {
      if (onRequireLogin) {
        onRequireLogin('Please sign in to complete your food order!');
      }
      return;
    }

    if (!deliveryAddress.trim() || !customerPhone.trim()) {
      setError('Please provide your delivery address and phone number.');
      return;
    }

    setLoading(true);
    setError(null);
    setPlacedOrder(null);

    const orderPayload = {
      restaurant_id: 1,
      customer_id: 1,
      order_type: 'DELIVERY',
      subtotal: subtotal,
      tax: tax,
      delivery_fee: deliveryFee,
      discount: 0,
      total_amount: grandTotal,
      delivery_address: `${deliveryAddress.trim()} (Phone: ${customerPhone.trim()})`,
      payment_status: 'PAID'
    };

    try {
      const order = await createOrder(orderPayload);
      setPlacedOrder(order);
      onClearCart();
    } catch (err) {
      setError('Failed to place order. Ensure backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div 
        className="modal-content" 
        style={{ maxWidth: '460px', right: 0, position: 'fixed', height: '100vh', borderRadius: 0 }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #edf2f7', paddingBottom: '16px' }}>
          <h3 style={{ margin: 0, fontFamily: 'var(--font-heading)', fontSize: '20px' }}>🛒 Your Food Cart</h3>
          <button onClick={onClose} style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}>✕</button>
        </div>

        {placedOrder ? (
          <div style={{ padding: '30px 10px', textAlign: 'center' }}>
            <span style={{ fontSize: '48px' }}>🎉</span>
            <h3 style={{ color: '#2e7d32', margin: '12px 0 6px' }}>Order Placed Successfully!</h3>
            <p style={{ color: '#718096', fontSize: '14px' }}>Your kitchen is already preparing the delicious food.</p>
            
            <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '8px', margin: '20px 0', border: '1px dashed #cbd5e1' }}>
              <span style={{ fontSize: '12px', color: '#718096' }}>TRACKING NUMBER</span>
              <h2 style={{ color: '#e65100', margin: '4px 0' }}>{placedOrder.order_number}</h2>
              <small style={{ color: '#718096' }}>You can copy this number to the Track tab or ask our AI Agent!</small>
            </div>

            <button className="submit-btn" style={{ width: '100%' }} onClick={onClose}>
              Continue Dining
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100% - 70px)' }}>
            {cart.length === 0 ? (
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', color: '#a0aec0' }}>
                <span style={{ fontSize: '42px', marginBottom: '8px' }}>🍽️</span>
                <p>Your cart is empty.</p>
                <small>Explore our Biryanis & Starters!</small>
              </div>
            ) : (
              <>
                <div style={{ flex: 1, overflowY: 'auto', padding: '16px 0' }}>
                  {cart.map((item) => (
                    <div key={item.id} className="cart-item-row">
                      <div style={{ flex: 1 }}>
                        <h4 style={{ margin: 0, fontSize: '15px', color: 'var(--dark)' }}>{item.name}</h4>
                        <small style={{ color: '#718096' }}>₹{item.price} each</small>
                      </div>

                      {/* Quantity Controller (+ and - buttons) */}
                      <div className="cart-qty-ctrl">
                        <button 
                          className="qty-btn" 
                          onClick={() => onDecreaseQty(item.id)}
                          title="Decrease quantity"
                        >
                          −
                        </button>
                        <span className="qty-count">{item.quantity}</span>
                        <button 
                          className="qty-btn" 
                          onClick={() => onIncreaseQty(item)}
                          title="Increase quantity"
                        >
                          +
                        </button>
                      </div>

                      <span style={{ fontWeight: '800', minWidth: '70px', textAlign: 'right', fontSize: '15px' }}>
                        ₹{item.price * item.quantity}
                      </span>
                    </div>
                  ))}

                  {/* Delivery Address & Phone Inputs */}
                  <div style={{ marginTop: '16px', borderTop: '1px dashed #cbd5e1', paddingTop: '14px' }}>
                    <label style={{ fontSize: '12px', fontWeight: 'bold', color: '#4a5568', display: 'block', marginBottom: '4px' }}>
                      Contact Phone *
                    </label>
                    <input
                      type="tel"
                      required
                      placeholder="e.g. 9876543210"
                      value={customerPhone}
                      onChange={(e) => setCustomerPhone(e.target.value)}
                      style={{ width: '100%', padding: '9px 12px', borderRadius: '6px', border: '1px solid #cbd5e1', marginBottom: '10px', fontSize: '13.5px' }}
                    />

                    <label style={{ fontSize: '12px', fontWeight: 'bold', color: '#4a5568', display: 'block', marginBottom: '4px' }}>
                      Delivery Address *
                    </label>
                    <textarea
                      rows="2"
                      required
                      placeholder="e.g. Flat 302, Green Meadows, Madhapur"
                      value={deliveryAddress}
                      onChange={(e) => setDeliveryAddress(e.target.value)}
                      style={{ width: '100%', padding: '9px 12px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '13.5px' }}
                    />
                  </div>
                </div>

                <div style={{ borderTop: '1px solid #edf2f7', paddingTop: '14px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '6px' }}>
                    <span>Item Total</span>
                    <span>₹{subtotal}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '6px' }}>
                    <span>GST (5%)</span>
                    <span>₹{tax}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '10px' }}>
                    <span>Delivery Fee</span>
                    <span>{deliveryFee === 0 ? <strong style={{ color: '#2e7d32' }}>FREE</strong> : `₹${deliveryFee}`}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '18px', fontWeight: '800', borderTop: '1px dashed #cbd5e1', paddingTop: '10px', marginBottom: '14px' }}>
                    <span>To Pay</span>
                    <span style={{ color: '#e65100' }}>₹{grandTotal}</span>
                  </div>

                  {error && <p style={{ color: '#c62828', fontSize: '12px', textAlign: 'center', marginBottom: '8px' }}>{error}</p>}

                  {/* Clear Book / Place Order Button */}
                  <button 
                    className="submit-btn" 
                    style={{ width: '100%', padding: '14px', fontSize: '16px' }} 
                    onClick={handleCheckout} 
                    disabled={loading}
                  >
                    {loading ? 'Processing Order...' : `Book / Place Order (₹${grandTotal}) 🚀`}
                  </button>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
