import React, { useEffect } from 'react';

export default function Toast({ toast, onClose }) {
  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => {
      onClose();
    }, 6000);
    return () => clearTimeout(timer);
  }, [toast, onClose]);

  if (!toast) return null;

  return (
    <div className="toast-floating-container">
      <div className={`toast-card ${toast.type || 'warning'}`}>
        <div className="toast-icon-wrap">
          <span>{toast.icon || '🔒'}</span>
        </div>
        <div className="toast-body">
          <div className="toast-title">{toast.title || 'Sign In Required'}</div>
          <div className="toast-message">{toast.message}</div>
        </div>
        {toast.actionLabel && toast.onAction && (
          <button
            className="toast-action-btn"
            onClick={() => {
              toast.onAction();
              onClose();
            }}
          >
            {toast.actionLabel}
          </button>
        )}
        <button className="toast-close-btn" onClick={onClose} title="Dismiss">
          ✕
        </button>
      </div>
    </div>
  );
}
