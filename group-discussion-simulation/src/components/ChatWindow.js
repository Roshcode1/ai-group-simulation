import React from 'react';
import './ChatWindow.css';

const ChatWindow = ({ messages }) => {
  return (
    <div className="chat-window">
      {messages.map((message, index) => (
        <div key={index} className={`message ${message.sender}`}>
          <span className="message-sender">{message.sender}: </span>
          <span className="message-text">{message.text}</span>
        </div>
      ))}
    </div>
  );
};

export default ChatWindow;
