import React, { useState } from 'react';
import './MessageInput.css';

const MessageInput = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');

  const handleSendMessage = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <div className="message-input-container">
      <input
        type="text"
        placeholder="Type your message..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
        className="message-input"
      />
      <button onClick={handleSendMessage} className="send-button">
        Send
      </button>
    </div>
  );
};

export default MessageInput;
