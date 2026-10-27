import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/api';

const QUICK_PROMPTS = [
  '🛵 I want to order food for delivery',
  '🍛 What Biryanis do you have?',
  '⏰ What are your opening hours?',
  '🪑 Book table for 2 tomorrow at 8 PM',
  '📦 Where is my order ORD-98765?'
];

export default function FloatingChat({ user, onRequireLogin }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: 'Namaste! 🙏 Welcome to Spice Garden. I am your autonomous AI Concierge. I can take food home delivery orders, check your live order status, answer menu questions, or book a table for you! How can I help you today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) scrollToBottom();
  }, [messages, isOpen]);

  useEffect(() => {
    const handleOpenAiChat = (e) => {
      if (!user) {
        if (onRequireLogin) {
          onRequireLogin('Please sign in to use the AI Concierge for ordering & tracking!');
        }
        return;
      }
      setIsOpen(true);
      if (e.detail?.prompt) {
        handleSend(e.detail.prompt);
      }
    };
    window.addEventListener('open-ai-chat', handleOpenAiChat);
    return () => window.removeEventListener('open-ai-chat', handleOpenAiChat);
  }, [messages, user, onRequireLogin]);

  const handleOpenClick = () => {
    if (!user) {
      if (onRequireLogin) {
        onRequireLogin('Please sign in to chat with our Autonomous AI Assistant!');
      }
      return;
    }
    setIsOpen(!isOpen);
  };

  const handleSend = async (messageText) => {
    if (!user) {
      if (onRequireLogin) {
        onRequireLogin('Please sign in to chat with our AI Assistant!');
      }
      return;
    }

    const textToSend = messageText || input;
    if (!textToSend.trim() || loading) return;

    // Add user message
    const userMsg = { sender: 'user', text: textToSend };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInput('');
    setLoading(true);

    try {
      // Pass the last 6 messages as conversation context
      const historyToSend = messages.slice(-6).map(m => ({
        sender: m.sender,
        text: m.text
      }));
      const data = await sendChatMessage(textToSend, historyToSend);
      setMessages((prev) => [...prev, { sender: 'bot', text: data.reply }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: '⚠️ Sorry, I could not connect to the backend server. Please make sure FastAPI is running on port 8000.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating Action Button with Up/Down Bobbing Movement & Callout Pill */}
      <div className="ai-fab-container">
        {!isOpen && (
          <div className="ai-fab-callout" onClick={handleOpenClick}>
            <span className="ai-fab-callout-badge">⚡ AI Concierge</span>
            <span className="ai-fab-callout-text">
              {user ? 'Use AI to Order / Track' : '🔒 Sign In to Use AI'}
            </span>
            <span className="ai-fab-callout-arrow">👉</span>
          </div>
        )}

        <button
          className="ai-fab"
          onClick={handleOpenClick}
          title={user ? 'Chat with AI Agent - Use AI to Order / Track' : 'Sign in required to chat with AI'}
          aria-label="Open AI Assistant"
        >
          <span>🤖</span>
          <div className="ai-fab-badge" />
        </button>
      </div>

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <div className="chat-header-title">
              <span style={{ fontSize: '22px' }}>✨</span>
              <div>
                <h4>Spice Garden AI Agent</h4>
                <span>● RAG & Autonomous Actions Online</span>
              </div>
            </div>
            <button className="close-chat-btn" onClick={() => setIsOpen(false)}>✕</button>
          </div>

          {/* Messages */}
          <div className="chat-messages">
            {messages.map((m, index) => (
              <div key={index} className={`chat-bubble ${m.sender}`}>
                {m.text.split('\n').map((line, i) => (
                  <p key={i} style={{ margin: line ? '4px 0' : '8px 0' }}>{line}</p>
                ))}
              </div>
            ))}
            {loading && (
              <div className="chat-bubble bot" style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#718096' }}>
                <span className="dot-pulse">●</span> Thinking & querying database...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Prompts */}
          <div className="chat-chips-area">
            {QUICK_PROMPTS.map((prompt, i) => (
              <button
                key={i}
                className="chat-chip"
                onClick={() => handleSend(prompt.replace(/^[^\s]+\s/, ''))}
              >
                {prompt}
              </button>
            ))}
          </div>

          {/* Input Box */}
          <form
            className="chat-input-bar"
            onSubmit={(e) => { e.preventDefault(); handleSend(); }}
          >
            <input
              type="text"
              placeholder="Ask about menu, order status, or book a table..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
            />
            <button type="submit" className="chat-send-btn" disabled={loading || !input.trim()}>
              ➤
            </button>
          </form>
        </div>
      )}
    </>
  );
}
