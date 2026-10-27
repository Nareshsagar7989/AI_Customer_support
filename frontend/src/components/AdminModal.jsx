import React, { useState, useEffect } from 'react';
import { addMenuItem, getCategories } from '../services/api';

export default function AdminModal({ isOpen, onClose, onDishAdded }) {
  const [categories, setCategories] = useState([]);
  const [dish, setDish] = useState({
    restaurant_id: 1,
    category_id: 1,
    name: '',
    description: '',
    price: 350,
    image_url: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&auto=format&fit=crop&q=60',
    is_vegetarian: false,
    is_vegan: false,
    spice_level: 'Medium',
    ingredients: '',
    allergens: '',
    is_available: true,
    preparation_time: 20
  });

  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  useEffect(() => {
    if (isOpen) {
      getCategories(1)
        .then((cats) => {
          setCategories(cats);
          if (cats.length > 0) {
            setDish((d) => ({ ...d, category_id: cats[0].id }));
          }
        })
        .catch(console.error);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg(null);
    setSuccessMsg(null);

    try {
      const created = await addMenuItem({
        ...dish,
        price: parseFloat(dish.price),
        category_id: parseInt(dish.category_id, 10),
        preparation_time: parseInt(dish.preparation_time, 10)
      });

      setSuccessMsg(`🎉 "${created.name}" saved to MySQL and dynamically synced to ChromaDB AI Knowledge Base!`);
      if (onDishAdded) onDishAdded();
      setTimeout(() => {
        setSuccessMsg(null);
        onClose();
      }, 2000);
    } catch (err) {
      setErrorMsg('Failed to add dish. Please check backend API.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <div>
            <h3 style={{ margin: 0, fontSize: '20px', fontFamily: 'var(--font-heading)' }}>
              👑 Admin: Add Food Item
            </h3>
            <small style={{ color: '#718096' }}>
              Real-time sync to MySQL and ChromaDB Vector Store
            </small>
          </div>
          <button 
            onClick={onClose} 
            style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}
          >
            ✕
          </button>
        </div>

        {successMsg && (
          <div style={{ background: '#e8f5e9', color: '#2e7d32', padding: '12px', borderRadius: '8px', marginBottom: '16px', fontWeight: 'bold' }}>
            {successMsg}
          </div>
        )}

        {errorMsg && (
          <div style={{ background: '#ffebee', color: '#c62828', padding: '12px', borderRadius: '8px', marginBottom: '16px' }}>
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="form-grid">
          <div className="form-group full-width">
            <label>Dish Name</label>
            <input
              type="text"
              required
              placeholder="e.g. Gongura Mutton Biryani"
              value={dish.name}
              onChange={(e) => setDish({ ...dish, name: e.target.value })}
            />
          </div>

          <div className="form-group">
            <label>Category (from MySQL)</label>
            <select
              value={dish.category_id}
              onChange={(e) => setDish({ ...dish, category_id: e.target.value })}
            >
              {categories.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Price (₹)</label>
            <input
              type="number"
              required
              min="10"
              value={dish.price}
              onChange={(e) => setDish({ ...dish, price: e.target.value })}
            />
          </div>

          <div className="form-group">
            <label>Spice Level</label>
            <select
              value={dish.spice_level}
              onChange={(e) => setDish({ ...dish, spice_level: e.target.value })}
            >
              <option value="Mild">Mild</option>
              <option value="Medium">Medium</option>
              <option value="High">High (Spicy)</option>
              <option value="Sweet">Sweet</option>
            </select>
          </div>

          <div className="form-group">
            <label>Dietary Type</label>
            <div style={{ display: 'flex', gap: '16px', marginTop: '8px' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '14px', cursor: 'pointer' }}>
                <input
                  type="checkbox"
                  checked={dish.is_vegetarian}
                  onChange={(e) => setDish({ ...dish, is_vegetarian: e.target.checked })}
                />
                Vegetarian
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '14px', cursor: 'pointer' }}>
                <input
                  type="checkbox"
                  checked={dish.is_vegan}
                  onChange={(e) => setDish({ ...dish, is_vegan: e.target.checked })}
                />
                Vegan
              </label>
            </div>
          </div>

          <div className="form-group full-width">
            <label>Image URL</label>
            <input
              type="url"
              placeholder="https://images.unsplash.com/..."
              value={dish.image_url}
              onChange={(e) => setDish({ ...dish, image_url: e.target.value })}
            />
          </div>

          <div className="form-group full-width">
            <label>Description (AI will use this for RAG)</label>
            <textarea
              rows="2"
              placeholder="Aromatic dish details, cooking style, taste notes..."
              value={dish.description}
              onChange={(e) => setDish({ ...dish, description: e.target.value })}
            />
          </div>

          <div className="form-group full-width">
            <label>Ingredients & Allergens</label>
            <input
              type="text"
              placeholder="e.g. Contains Cashews, Ghee, Dairy"
              value={dish.allergens}
              onChange={(e) => setDish({ ...dish, allergens: e.target.value })}
            />
          </div>

          <button
            type="submit"
            className="submit-btn"
            style={{ gridColumn: 'span 2' }}
            disabled={loading}
          >
            {loading ? 'Adding & Syncing to ChromaDB...' : 'Add Dish & Sync to AI Agent ⚡'}
          </button>
        </form>
      </div>
    </div>
  );
}
