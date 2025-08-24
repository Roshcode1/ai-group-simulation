import React from 'react';
import './Character.css';

const Character = ({ character }) => {
  return (
    <div className="character-container">
      <img src={character.avatar} alt={character.name} className="character-avatar" />
      <span className="character-name">{character.name}</span>
    </div>
  );
};

export default Character;
