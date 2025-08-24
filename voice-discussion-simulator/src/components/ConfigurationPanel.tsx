import React, { useState } from 'react';
import styled from 'styled-components';
import { Character, ApiConfig, AudioState } from '../types';

const Panel = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  height: 100%;
  overflow-y: auto;
`;

const Section = styled.div`
  margin-bottom: 24px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
`;

const SectionTitle = styled.h3`
  margin: 0 0 16px 0;
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #ffffff;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;

  &:focus {
    border-color: #e94560;
    box-shadow: 0 0 0 2px rgba(233, 69, 96, 0.2);
  }

  &::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }
`;

const Button = styled.button<{ variant?: 'primary' | 'secondary' | 'success' | 'danger' }>`
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-width: 120px;

  background: ${props => {
    switch (props.variant) {
      case 'success': return '#4ade80';
      case 'danger': return '#f87171';
      case 'secondary': return 'rgba(255, 255, 255, 0.1)';
      default: return '#e94560';
    }
  }};

  color: #ffffff;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 12px;
  margin-top: 16px;
`;

const CharacterItem = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  margin-bottom: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
`;

const CharacterColor = styled.div<{ color: string }>`
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: ${props => props.color};
  flex-shrink: 0;
`;

const CharacterInfo = styled.div`
  flex: 1;
`;

const CharacterName = styled.div`
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 4px;
`;

const CharacterPersonality = styled.div`
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
`;

const Checkbox = styled.input`
  width: 18px;
  height: 18px;
  accent-color: #e94560;
`;

const UserInputSection = styled.div`
  margin-top: 16px;
`;

const UserInputGroup = styled.div`
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
`;

const UserInputField = styled.input`
  flex: 1;
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: #ffffff;
  font-size: 14px;
  outline: none;

  &:focus {
    border-color: #e94560;
  }
`;

const SmallButton = styled.button<{ variant?: 'primary' | 'secondary' }>`
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  background: ${props => props.variant === 'secondary' ? 'rgba(255, 255, 255, 0.1)' : '#e94560'};
  color: #ffffff;

  &:hover {
    transform: translateY(-1px);
  }
`;

const StatusText = styled.div<{ isConnected: boolean }>`
  color: ${props => props.isConnected ? '#4ade80' : '#f87171'};
  font-size: 12px;
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
`;

interface ConfigurationPanelProps {
  topic: string;
  onTopicChange: (topic: string) => void;
  characters: Character[];
  activeCharacters: string[];
  onCharacterToggle: (characterId: string, isActive: boolean) => void;
  isDiscussionActive: boolean;
  onStartDiscussion: () => void;
  onStopDiscussion: () => void;
  onSaveDiscussion: () => void;
  apiConfig: ApiConfig;
  onTestApi: () => void;
  audioState: AudioState;
  onVoiceRecording: () => void;
  onAddUserMessage: (message: string, useTTS: boolean) => void;
}

const ConfigurationPanel: React.FC<ConfigurationPanelProps> = ({
  topic,
  onTopicChange,
  characters,
  activeCharacters,
  onCharacterToggle,
  isDiscussionActive,
  onStartDiscussion,
  onStopDiscussion,
  onSaveDiscussion,
  apiConfig,
  onTestApi,
  audioState,
  onVoiceRecording,
  onAddUserMessage
}) => {
  const [userInput, setUserInput] = useState('');

  const handleSendMessage = (useTTS: boolean = false) => {
    if (userInput.trim()) {
      onAddUserMessage(userInput.trim(), useTTS);
      setUserInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSendMessage(false);
    }
  };

  return (
    <Panel>
      {/* API Configuration */}
      <Section>
        <SectionTitle>🔑 API Configuration</SectionTitle>
        <div style={{ marginBottom: '12px' }}>
          <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.7)', marginBottom: '4px' }}>
            API Key: sk_...{apiConfig.apiKey.slice(-8)}
          </div>
          <StatusText isConnected={apiConfig.isConnected}>
            {apiConfig.isConnected ? '✅ Connected' : '❌ Disconnected'}
          </StatusText>
        </div>
        <Button onClick={onTestApi} variant="secondary">
          🧪 Test Connection
        </Button>
      </Section>

      {/* Discussion Topic */}
      <Section>
        <SectionTitle>📝 Discussion Topic</SectionTitle>
        <Input
          type="text"
          value={topic}
          onChange={(e) => onTopicChange(e.target.value)}
          placeholder="Enter discussion topic..."
          disabled={isDiscussionActive}
        />
      </Section>

      {/* AI Characters */}
      <Section>
        <SectionTitle>👥 AI Characters</SectionTitle>
        {characters.map((character) => (
          <CharacterItem key={character.id}>
            <CharacterColor color={character.color} />
            <CharacterInfo>
              <CharacterName>{character.name}</CharacterName>
              <CharacterPersonality>{character.personality}</CharacterPersonality>
            </CharacterInfo>
            <Checkbox
              type="checkbox"
              checked={activeCharacters.includes(character.id)}
              onChange={(e) => onCharacterToggle(character.id, e.target.checked)}
              disabled={isDiscussionActive}
            />
          </CharacterItem>
        ))}
      </Section>

      {/* Controls */}
      <Section>
        <SectionTitle>🎮 Controls</SectionTitle>
        <ButtonGroup>
          {!isDiscussionActive ? (
            <Button onClick={onStartDiscussion} variant="success" disabled={!apiConfig.isConnected}>
              🚀 Start Discussion
            </Button>
          ) : (
            <Button onClick={onStopDiscussion} variant="danger">
              ⏹️ Stop Discussion
            </Button>
          )}
        </ButtonGroup>
      </Section>

      {/* User Input Section */}
      <Section>
        <SectionTitle>💬 Your Response</SectionTitle>
        <UserInputSection>
          <UserInputGroup>
            <UserInputField
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={!isDiscussionActive}
            />
          </UserInputGroup>
          
          <ButtonGroup>
            <SmallButton 
              onClick={() => handleSendMessage(false)}
              disabled={!userInput.trim() || !isDiscussionActive}
            >
              📤 Send
            </SmallButton>
            <SmallButton 
              onClick={() => handleSendMessage(true)}
              variant="secondary"
              disabled={!userInput.trim() || !isDiscussionActive}
            >
              🔊 Speak
            </SmallButton>
          </ButtonGroup>

          <Button
            onClick={onVoiceRecording}
            variant="secondary"
            disabled={!isDiscussionActive}
            style={{ marginTop: '12px', width: '100%' }}
          >
            {audioState.isRecording ? '⏹️ Stop Recording' : '🎤 Record Voice'}
          </Button>
        </UserInputSection>
      </Section>

      {/* Save button */}
      <Section>
        <SectionTitle>💾 Save Discussion</SectionTitle>
        <Button onClick={onSaveDiscussion} variant="secondary" style={{ width: '100%' }}>
          💾 Export Discussion
        </Button>
      </Section>
    </Panel>
  );
};

export default ConfigurationPanel;