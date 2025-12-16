/**
 * ChatInterface Component
 * A React component for the RAG chatbot interface in Docusaurus
 */

import React, { useState, useEffect, useRef } from 'react';
import apiConfig from './apiConfig'; // Import the centralized API config
import './ChatInterface.css'; // Assuming you have custom styles

const ChatInterface = ({ docsDir }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [selectedText, setSelectedText] = useState(null);
  const [mode, setMode] = useState('global'); // 'global' or 'selected_text'
  const messagesEndRef = useRef(null);

  // Function to scroll to the bottom of the chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
        setMode('selected_text');
      } else if (mode === 'selected_text') {
        // If we were in selected text mode and no text is selected anymore, switch to global
        setMode('global');
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, [mode]);

  // Function to send a message to the backend
  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare the request body - only send message as requested
      const requestBody = {
        message: inputValue
      };

      // Make the API call to the backend
      const response = await fetch(apiConfig.baseUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update session ID if this is the first message
      if (!sessionId) {
        setSessionId(data.session_id);
      }

      // Add AI response to the chat
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        context: data.context, // Store context if needed for display
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Function to clear the chat
  const clearChat = () => {
    setMessages([]);
    setSessionId(null);
    if (mode === 'selected_text') {
      setMode('global');
      setSelectedText(null);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>RAG Chatbot</h3>
        <div className="chat-mode-indicator">
          Mode: <span className={mode === 'global' ? 'global-mode' : 'selected-mode'}>
            {mode === 'global' ? 'Global (All Docs)' : 'Focused (Selected Text)'}
          </span>
        </div>
        <button onClick={clearChat} className="clear-chat-btn">Clear Chat</button>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your documentation assistant.</p>
            <p>
              {mode === 'global' 
                ? "Ask me anything about the documentation. I'll search through all available documents to find the answer."
                : `I'm focused on the text you selected: "${selectedText?.substring(0, 50)}...". Ask me questions about this specific content.`}
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div 
              key={message.id} 
              className={`message ${message.role === 'user' ? 'user-message' : 'ai-message'}`}
            >
              <div className="message-content">
                {message.content}
              </div>
              <div className="message-timestamp">
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message ai-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        {mode === 'selected_text' && (
          <div className="selected-text-preview">
            <strong>Selected:</strong> "{selectedText?.substring(0, 100)}..."
          </div>
        )}
        <div className="input-controls">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={
              mode === 'global' 
                ? "Ask a question about the documentation..." 
                : "Ask a question about the selected text..."
            }
            disabled={isLoading}
            className="chat-input"
            rows="3"
          />
          <button 
            onClick={sendMessage} 
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
        <div className="chat-controls">
          <button 
            onClick={() => {
              setMode(mode === 'global' ? 'selected_text' : 'global');
              if (mode === 'selected_text') setSelectedText(null);
            }}
            className={`mode-toggle ${mode === 'global' ? 'active' : ''}`}
          >
            Global Mode
          </button>
          <button 
            onClick={() => {
              if (!selectedText) {
                alert('Please select text in the documentation first');
                return;
              }
              setMode('selected_text');
            }}
            className={`mode-toggle ${mode === 'selected_text' ? 'active' : ''}`}
            disabled={!selectedText}
          >
            Focused Mode
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;