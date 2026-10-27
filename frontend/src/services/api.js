const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export async function getMenu(restaurantId = 1) {
  const res = await fetch(`${API_BASE_URL}/menu/${restaurantId}`);
  if (!res.ok) throw new Error('Failed to fetch menu');
  return res.json();
}

export async function getCategories(restaurantId = 1) {
  const res = await fetch(`${API_BASE_URL}/menu/categories/${restaurantId}`);
  if (!res.ok) throw new Error('Failed to fetch categories');
  return res.json();
}

export async function addMenuItem(itemData) {
  const res = await fetch(`${API_BASE_URL}/menu/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(itemData),
  });
  if (!res.ok) throw new Error('Failed to add menu item');
  return res.json();
}

export async function sendChatMessage(message, history = []) {
  const res = await fetch(`${API_BASE_URL}/chat/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history }),
  });
  if (!res.ok) throw new Error('Failed to send message to AI');
  return res.json();
}

export async function bookTable(reservationData) {
  const res = await fetch(`${API_BASE_URL}/reservations/book`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reservationData),
  });
  if (!res.ok) throw new Error('Failed to book table');
  return res.json();
}

export async function createOrder(orderData) {
  const res = await fetch(`${API_BASE_URL}/orders/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(orderData),
  });
  if (!res.ok) throw new Error('Failed to place order');
  return res.json();
}

export async function getOrders(restaurantId = 1) {
  const res = await fetch(`${API_BASE_URL}/orders/${restaurantId}`);
  if (!res.ok) throw new Error('Failed to fetch orders');
  return res.json();
}

export async function loginUser(credentials) {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Login failed');
  return data;
}

export async function registerUser(userData) {
  const res = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Registration failed');
  return data;
}

export async function getOrderHistory(phone = '') {
  const url = phone ? `${API_BASE_URL}/orders/history/list?phone=${encodeURIComponent(phone)}` : `${API_BASE_URL}/orders/history/list`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch order history');
  return res.json();
}
