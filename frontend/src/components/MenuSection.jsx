import React, { useState, useEffect } from 'react';
import { getCategories } from '../services/api';

export default function MenuSection({ menuItems, cart = [], onAddToCart, onDecreaseQty }) {
  const [categories, setCategories] = useState([]);
  const [selectedCatId, setSelectedCatId] = useState('ALL');
  const [vegOnly, setVegOnly] = useState(false);

  useEffect(() => {
    async function loadCategories() {
      try {
        const cats = await getCategories(1);
        setCategories(cats);
      } catch (err) {
        console.error('Failed to load categories:', err);
      }
    }
    loadCategories();
  }, []);

  const filteredItems = menuItems.filter((item) => {
    const matchesCat = selectedCatId === 'ALL' || item.category_id === selectedCatId;
    const matchesVeg = !vegOnly || item.is_vegetarian;
    return matchesCat && matchesVeg;
  });

  return (
    <div>
      {/* Dynamic Filters from MySQL */}
      <div className="filter-bar">
        <div className="category-chips">
          <button
            className={`chip ${selectedCatId === 'ALL' ? 'active' : ''}`}
            onClick={() => setSelectedCatId('ALL')}
          >
            All Items
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              className={`chip ${selectedCatId === cat.id ? 'active' : ''}`}
              onClick={() => setSelectedCatId(cat.id)}
            >
              {cat.name}
            </button>
          ))}
        </div>

        <label className="veg-toggle">
          <input
            type="checkbox"
            checked={vegOnly}
            onChange={(e) => setVegOnly(e.target.checked)}
          />
          <span style={{ color: '#2e7d32' }}>🌱 Pure Veg Only</span>
        </label>
      </div>

      {/* Dynamic Food Cards Grid */}
      {filteredItems.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '60px 20px', color: '#718096' }}>
          <h3>No dishes found matching your criteria.</h3>
          <p>Try switching category or turning off the veg-only filter!</p>
        </div>
      ) : (
        <div className="food-grid">
          {filteredItems.map((item) => {
            const inCart = cart.find((c) => c.id === item.id);

            return (
              <div key={item.id} className="food-card">
                <div className="food-img-wrap">
                  <img
                    src={
                      item.image_url ||
                      'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&auto=format&fit=crop&q=60'
                    }
                    alt={item.name}
                    loading="lazy"
                    onError={(e) => {
                      e.target.src =
                        'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&auto=format&fit=crop&q=60';
                    }}
                  />

                  {/* Veg / Non-Veg Icon */}
                  <div className="dietary-badge" title={item.is_vegetarian ? 'Vegetarian' : 'Non-Vegetarian'}>
                    <div className={item.is_vegetarian ? 'veg-icon' : 'non-veg-icon'} />
                  </div>

                  {/* Spice Level */}
                  {item.spice_level && (
                    <div className="spice-tag">
                      🌶️ {item.spice_level}
                    </div>
                  )}
                </div>

                <div className="food-details">
                  <h3 className="food-title">{item.name}</h3>
                  <p className="food-desc">{item.description || 'Freshly prepared specialty with authentic spices.'}</p>

                  <div className="food-footer">
                    <span className="price-tag">₹{Math.round(item.price)}</span>

                    {/* If item in cart, show Swiggy-style - [qty] + controls, else show + ADD */}
                    {inCart ? (
                      <div className="cart-qty-ctrl">
                        <button 
                          className="qty-btn" 
                          onClick={() => onDecreaseQty(item.id)}
                          title="Decrease"
                        >
                          −
                        </button>
                        <span className="qty-count">{inCart.quantity}</span>
                        <button 
                          className="qty-btn" 
                          onClick={() => onAddToCart(item)}
                          title="Increase"
                        >
                          +
                        </button>
                      </div>
                    ) : (
                      <button
                        className="add-btn"
                        onClick={() => onAddToCart(item)}
                      >
                        + ADD
                      </button>
                    )}
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
