import React, { useState, useEffect, useRef } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import { v4 as uuidv4 } from 'uuid';
import apiConfig from './apiConfig'; // Import the centralized API config
import './ChatWidget.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const { colorMode } = useColorMode();
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();

    // Initialize or retrieve session ID from localStorage
    let currentSessionId = localStorage.getItem('chat_session_id');
    if (!currentSessionId) {
      // Create a new UUID session ID
      currentSessionId = uuidv4();
      localStorage.setItem('chat_session_id', currentSessionId);
    }
    setSessionId(currentSessionId);

    // Event listener to capture selected text on the page
    const handleSelectionChange = () => {
      const selection = window.getSelection();
      if (selection.toString().trim()) {
        setSelectedText(selection.toString().trim());
      } else {
        setSelectedText('');
      }
    };

    document.addEventListener('mouseup', handleSelectionChange);
    document.addEventListener('keyup', handleSelectionChange);

    return () => {
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('keyup', handleSelectionChange);
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { role: 'user', content: inputValue.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const requestBody = {
        message: userMessage.content,
        selected_text: selectedText || null,  // Include selected text if available
        mode: selectedText ? "selected_text" : "global",
        session_id: sessionId || null,
        user_id: null  // No user auth required
      };

      const response = await fetch(apiConfig.baseUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, ${errorText}`);
      }

      const data = await response.json();

      // Update the session ID if the backend has generated a new one
      if (data.session_id && data.session_id !== sessionId) {
        setSessionId(data.session_id);
        localStorage.setItem('chat_session_id', data.session_id);
      }

      const botMessage = {
        role: 'bot',
        content: data.response,
        sources: data.context  // Use context as sources
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Full error details:', error);
      let errorMessageText = 'Sorry, I encountered an error. Please try again.';

      // Provide more specific error messages
      if (error.message.includes('fetch')) {
        errorMessageText = 'Network error: Could not reach the chatbot server. Please make sure the backend is running.';
      } else if (error.message.includes('HTTP')) {
        errorMessageText = `Server error: ${error.message}`;
      } else {
        errorMessageText = `Error: ${error.message || error}`;
      }

      const errorMessage = {
        role: 'bot',
        content: errorMessageText
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  const handleUseSelectedText = () => {
    if (selectedText) {
      setInputValue(`Based on the selected text: "${selectedText}", ${inputValue}`);
    } else {
      alert("No text is currently selected. Please select text on the page first.");
    }
  };

  return (
    <>
      {isOpen ? (
        <div className={`chat-widget ${colorMode}`}>
          <div className="chat-header">
            <span>Robotics Assistant</span>
            <button className="close-button" onClick={closeChat}>×</button>
          </div>
          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <p>Hello! I'm your Robotics Assistant.</p>
                <p>Ask me anything about Physical AI & Humanoid Robotics.</p>
                <p>Select text in the book and ask questions about it!</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div key={index} className={`message ${msg.role}`}>
                  {msg.content}
                  {msg.sources && msg.sources.length > 0 && (
                    <details className="sources-details">
                      <summary>Sources</summary>
                      <ul>
                        {msg.sources.map((source, idx) => (
                          <li key={idx}>{source.fileName}</li>
                        ))}
                      </ul>
                    </details>
                  )}
                </div>
              ))
            )}
            {isLoading && (
              <div className="message bot">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className="selected-text-info">
            {selectedText && (
              <small className="selected-preview">Selected: "{selectedText.substring(0, 60)}..."</small>
            )}
          </div>
          <form onSubmit={handleSubmit} className="chat-input-form">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask about robotics..."
              disabled={isLoading}
              className="chat-input"
            />
            {selectedText && (
              <button
                type="button"
                onClick={handleUseSelectedText}
                className="use-selection-button"
                title="Include selected text in your question"
              >
                +
              </button>
            )}
            <button type="submit" disabled={!inputValue.trim() || isLoading} className="send-button">
              Send
            </button>
          </form>
        </div>
      ) : (
        <button className={`chat-toggle ${colorMode}`} onClick={toggleChat}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H17L14.25 19.75C14.05 19.95 13.79 20.07 13.5 20.07C13.21 20.07 12.95 19.95 12.75 19.75C12.55 19.55 12.42 19.29 12.42 19C12.42 18.71 12.55 18.45 12.75 18.25L15.5 15.5H19C19.5304 15.5 20.0391 15.2893 20.4142 14.9142C20.7893 14.5391 21 14.0304 21 13.5V15Z" fill="currentColor"/>
            <path d="M19 11H16.5L11.5 4.5L5.5 11H3C2.46957 11 1.96086 11.2107 1.58579 11.5858C1.21071 11.9609 1 12.4696 1 13V19C1 19.5304 1.21071 2.0391 1.58579 20.4142C1.96086 20.7893 2.46957 21 3 21H12.5C12.71 21 12.92 20.95 13.12 20.85C13.32 20.75 13.5 20.61 13.65 20.44L19.65 13.44C19.84 13.23 19.97 12.99 20.04 12.71C20.11 12.43 20.11 12.14 19.96 11.87L19.04 10.13C18.89 9.86 18.67 9.63 18.41 9.47C18.15 9.31 17.86 9.22 17.56 9.22H15.5L19 11Z" fill="currentColor"/>
          </svg>
        </button>
      )}
    </>
  );
};

export default ChatWidget;