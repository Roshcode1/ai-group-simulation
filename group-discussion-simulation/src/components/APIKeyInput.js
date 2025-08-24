import React from 'react';
import './APIKeyInput.css';

const APIKeyInput = ({ apiKey, setApiKey, placeholder }) => {
  return (
    <div className="api-key-input-container">
      <input
        type="text"
        placeholder={placeholder}
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        className="api-key-input"
      />
    </div>
  );
};

export default APIKeyInput;
