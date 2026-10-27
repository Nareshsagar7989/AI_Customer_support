import React, { useState, useEffect } from 'react';
import { getMenu } from './services/api';
import MenuSection from './components/MenuSection';
import DineInReservation from './components/DineInReservation';
import OrderTracking from './components/OrderTracking';
import OrdersHistory from './components/OrdersHistory';
import FloatingChat from './components/FloatingChat';
import CartDrawer from './components/CartDrawer';
import AdminModal from './components/AdminModal';
import Toast from './components/Toast';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

export default function App() {
  const [activeTab, setActiveTab] = useState('menu'); // 'menu' | 'dinein' | 'track' | 'orders'
  const [currentPage, setCurrentPage] = useState('app'); // 'app' | 'login' | 'register'
  const [registeredUser, setRegisteredUser] = useState('');
  const [regNotice, setRegNotice] = useState('');
  const [menuItems, setMenuItems] = useState([]);
  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isAdminOpen, setIsAdminOpen] = useState(false);
  const [toast, setToast] = useState(null);
  const [loadingMenu, setLoadingMenu] = useState(true);

  // Authenticated User State (Loaded from localStorage)
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      const saved = localStorage.getItem('spice_garden_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  const handleLoginSuccess = (user) => {
    setCurrentUser(user);
    localStorage.setItem('spice_garden_user', JSON.stringify(user));
    setCurrentPage('app');
    setToast({
      title: 'Signed In Successfully',
      message: `Welcome, ${user.name || user.username}! (${user.role})`,
      icon: user.role === 'ADMIN' ? '👑' : '👤',
      type: 'success'
    });
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem('spice_garden_user');
  };

  const fetchMenuItems = async () => {
    try {
      setLoadingMenu(true);
      const items = await getMenu(1);
      setMenuItems(items);
    } catch (err) {
      console.error('Error fetching menu:', err);
    } finally {
      setLoadingMenu(false);
    }
  };

  useEffect(() => {
    fetchMenuItems();
  }, []);

  const triggerAuthToast = (message = 'Please sign in to continue!') => {
    setToast({
      title: 'Sign In Required',
      message: message,
      icon: '🔒',
      type: 'warning',
      actionLabel: 'Sign In Now 👉',
      onAction: () => {
        setRegNotice('');
        setCurrentPage('login');
      }
    });
  };

  const handleAddToCart = (dish) => {
    if (!currentUser) {
      triggerAuthToast('Please sign in to add dishes to cart and place orders!');
      return;
    }
    setCart((prevCart) => {
      const existing = prevCart.find((i) => i.id === dish.id);
      if (existing) {
        return prevCart.map((i) =>
          i.id === dish.id ? { ...i, quantity: i.quantity + 1 } : i
        );
      }
      return [...prevCart, { ...dish, quantity: 1 }];
    });
  };

  const handleDecreaseQty = (dishId) => {
    setCart((prevCart) => {
      const existing = prevCart.find((i) => i.id === dishId);
      if (!existing) return prevCart;
      if (existing.quantity === 1) {
        return prevCart.filter((i) => i.id !== dishId);
      }
      return prevCart.map((i) =>
        i.id === dishId ? { ...i, quantity: i.quantity - 1 } : i
      );
    });
  };

  const totalCartCount = cart.reduce((acc, item) => acc + item.quantity, 0);

  const handleOpenCart = () => {
    if (!currentUser) {
      triggerAuthToast('Please sign in to view your cart and checkout!');
      return;
    }
    setIsCartOpen(true);
  };

  const handleTriggerAi = (prompt = '') => {
    if (!currentUser) {
      triggerAuthToast('Please sign in to use the AI Concierge for ordering & tracking!');
      return;
    }
    window.dispatchEvent(new CustomEvent('open-ai-chat', { detail: { prompt } }));
  };

  // 1. DEDICATED SIGN IN PAGE
  if (currentPage === 'login') {
    return (
      <>
        <LoginPage
          onLoginSuccess={handleLoginSuccess}
          onNavigateRegister={() => {
            setRegNotice('');
            setCurrentPage('register');
          }}
          onBackToHome={() => setCurrentPage('app')}
          prefilledUsername={registeredUser}
          initialSuccessMsg={regNotice}
        />
        <Toast toast={toast} onClose={() => setToast(null)} />
      </>
    );
  }

  // 2. DEDICATED REGISTER PAGE
  if (currentPage === 'register') {
    return (
      <>
        <RegisterPage
          onRegisterSuccess={(uname) => {
            setRegisteredUser(uname);
            setRegNotice(`✅ Account created for "${uname}"! Please enter your password to sign in.`);
            setCurrentPage('login');
          }}
          onNavigateLogin={() => {
            setRegNotice('');
            setCurrentPage('login');
          }}
          onBackToHome={() => setCurrentPage('app')}
        />
        <Toast toast={toast} onClose={() => setToast(null)} />
      </>
    );
  }

  // 3. MAIN RESTAURANT APP VIEW
  return (
    <div className="app-container">
      {/* 1. TOP STICKY PREMIERE GLASSMORPHIC NAVBAR */}
      <header className="navbar-sticky">
        <div className="navbar-container">
          {/* Left: Brand Identity */}
          <div className="nav-brand" onClick={() => setActiveTab('menu')}>
            <div className="nav-brand-logo">🌶️</div>
            <div className="nav-brand-text">
              <h1>Spice Garden</h1>
              <p>Authentic Royal Cuisine • Madhapur</p>
            </div>
          </div>

          {/* Center: Floating Capsule Segmented Tabs */}
          <nav className="nav-capsule-tabs">
            <button
              className={`nav-capsule-btn ${activeTab === 'menu' ? 'active' : ''}`}
              onClick={() => setActiveTab('menu')}
            >
              <span>🍛</span> Order Online
            </button>
            <button
              className={`nav-capsule-btn ${activeTab === 'dinein' ? 'active' : ''}`}
              onClick={() => setActiveTab('dinein')}
            >
              <span>🪑</span> Table Booking
            </button>
            <button
              className={`nav-capsule-btn ${activeTab === 'track' ? 'active' : ''}`}
              onClick={() => setActiveTab('track')}
            >
              <span>📦</span> Track Live Order
            </button>
            <button
              className={`nav-capsule-btn ${activeTab === 'orders' ? 'active' : ''}`}
              onClick={() => setActiveTab('orders')}
            >
              <span>📜</span> Orders
            </button>
          </nav>

          {/* Right: Actions Cluster (Admin + Cart + Auth/SignOut) */}
          <div className="nav-actions">
            {/* ADMIN SYNC BUTTON: ONLY visible if currentUser is ADMIN */}
            {currentUser?.role === 'ADMIN' && (
              <button
                className="nav-admin-btn"
                onClick={() => setIsAdminOpen(true)}
                title="Admin sync and add menu dish"
              >
                <span>👑</span> Admin Portal
              </button>
            )}

            {/* Glowing Cart Pill */}
            <button className="nav-cart-btn" onClick={handleOpenCart}>
              <span>🛒</span>
              <span>Cart</span>
              <span className="nav-cart-badge">{totalCartCount}</span>
            </button>

            {/* TOP RIGHT CORNER: Authentication Capsule */}
            {currentUser ? (
              <div className="nav-user-capsule">
                <div className="nav-user-info">
                  <span style={{ fontSize: '15px' }}>
                    {currentUser.role === 'ADMIN' ? '👑' : '👤'}
                  </span>
                  <span className="nav-user-name">
                    {currentUser.name || currentUser.username}
                  </span>
                  <span className={`nav-role-badge ${currentUser.role === 'ADMIN' ? 'admin' : 'customer'}`}>
                    {currentUser.role}
                  </span>
                </div>

                <button
                  className="nav-signout-btn"
                  onClick={handleLogout}
                  title="Sign Out of account"
                >
                  <span>🚪</span> Sign Out
                </button>
              </div>
            ) : (
              <div className="nav-auth-actions">
                <button
                  className="nav-signin-btn"
                  onClick={() => {
                    setRegNotice('');
                    setCurrentPage('login');
                  }}
                  title="Sign in with your credentials or 1-click recruiter demo"
                >
                  <span>🔑</span> Sign In
                </button>
                <button
                  className="nav-register-btn"
                  onClick={() => {
                    setRegNotice('');
                    setCurrentPage('register');
                  }}
                  title="Create new customer account"
                >
                  <span>✨</span> Register
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* 2. MODERN PREMIERE AI HERO SECTION - "USE AI TO ORDER / TRACK" */}
      <section className="restaurant-hero-ambient">
        <div className="hero-ambient-content">
          <div className="hero-headline">
            <div className="ai-hero-pill-badge">
              <span className="ai-pulse-dot"></span>
              <span>⚡ Autonomous Restaurant Agent Active • LLM + Vector RAG + Tool Calling</span>
            </div>

            <h2 className="ai-hero-title">
              Use <span className="highlight-ai-gradient">AI to Order / Track</span> & Reserve
            </h2>

            <p className="ai-hero-desc">
              Skip traditional menus! Chat naturally with our autonomous AI Agent to order food, track live delivery status in real-time, or book dining tables with zero human intervention.
            </p>

            <div className="ai-hero-actions-row">
              <button
                className="ai-hero-primary-btn"
                onClick={() => handleTriggerAi('')}
              >
                <span>🤖</span> Launch AI Assistant
              </button>

              <div className="ai-hero-quick-prompts">
                <span className="quick-prompt-label">Try Asking:</span>
                <button
                  className="ai-hero-prompt-chip"
                  onClick={() => handleTriggerAi('Order 1 Chicken Dum Biryani to Madhapur, Hyderabad')}
                >
                  🛵 "Order 1 Chicken Dum Biryani"
                </button>
                <button
                  className="ai-hero-prompt-chip"
                  onClick={() => handleTriggerAi('Where is my order status?')}
                >
                  📦 "Track my order"
                </button>
                <button
                  className="ai-hero-prompt-chip"
                  onClick={() => handleTriggerAi('Suggest spicy starters under ₹300')}
                >
                  ⚡ "Suggest spicy starters"
                </button>
                <button
                  className="ai-hero-prompt-chip"
                  onClick={() => handleTriggerAi('Reserve a table for 4 tomorrow at 8 PM')}
                >
                  🪑 "Book table for 4"
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Tab Content Area */}
      <main className="main-content">
        {activeTab === 'menu' && (
          <>
            <div style={{ marginBottom: '24px' }}>
              <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '26px', fontWeight: 800 }}>
                Explore Our Chef's Menu
              </h2>
              <p style={{ color: '#718096', fontSize: '14px' }}>
                Handcrafted Hyderabadi dum biryanis, smoky tandoori starters, and rich curries.
              </p>
            </div>

            {loadingMenu ? (
              <div style={{ textAlign: 'center', padding: '60px 20px', color: '#718096' }}>
                <div style={{ fontSize: '32px', marginBottom: '12px' }}>🍲</div>
                <p>Loading fresh dishes from MySQL database...</p>
              </div>
            ) : (
              <MenuSection
                menuItems={menuItems}
                cart={cart}
                onAddToCart={handleAddToCart}
                onDecreaseQty={handleDecreaseQty}
              />
            )}
          </>
        )}

        {activeTab === 'dinein' && (
          <DineInReservation
            user={currentUser}
            onRequireLogin={triggerAuthToast}
          />
        )}

        {activeTab === 'track' && <OrderTracking />}

        {activeTab === 'orders' && (
          <OrdersHistory
            user={currentUser}
            onOpenLogin={() => {
              setRegNotice('');
              setCurrentPage('login');
            }}
          />
        )}
      </main>

      {/* Floating Autonomous AI Assistant */}
      <FloatingChat
        user={currentUser}
        onRequireLogin={triggerAuthToast}
      />

      {/* Cart Drawer */}
      <CartDrawer
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        cart={cart}
        onClearCart={() => setCart([])}
        onIncreaseQty={handleAddToCart}
        onDecreaseQty={handleDecreaseQty}
        user={currentUser}
        onRequireLogin={triggerAuthToast}
      />

      {/* Admin Modal for Dynamic Dish Addition */}
      <AdminModal
        isOpen={isAdminOpen}
        onClose={() => setIsAdminOpen(false)}
        onDishAdded={fetchMenuItems}
      />

      {/* Interactive Floating Toast Notification */}
      <Toast toast={toast} onClose={() => setToast(null)} />
    </div>
  );
}
