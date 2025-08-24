import React, { useRef, useEffect } from 'react';
import styled from 'styled-components';
import { DiscussionState, AudioState } from '../types';
import { CHARACTERS } from '../constants/characters';

const Panel = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
`;

const PanelHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
`;

const PanelTitle = styled.h2`
  margin: 0;
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const DiscussionStatus = styled.div<{ isActive: boolean }>`
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  background: ${props => props.isActive ? 'rgba(74, 222, 128, 0.2)' : 'rgba(160, 160, 160, 0.2)'};
  color: ${props => props.isActive ? '#4ade80' : '#a0a0a0'};
  border: 1px solid ${props => props.isActive ? '#4ade80' : '#a0a0a0'};
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
  margin-bottom: 16px;

  /* Custom scrollbar */
  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }
`;

const Message = styled.div<{ type: 'user' | 'ai' }>`
  margin-bottom: 16px;
  padding: 16px;
  border-radius: 12px;
  background: ${props => props.type === 'user' 
    ? 'rgba(233, 69, 96, 0.1)' 
    : 'rgba(255, 255, 255, 0.05)'
  };
  border: 1px solid ${props => props.type === 'user' 
    ? 'rgba(233, 69, 96, 0.3)' 
    : 'rgba(255, 255, 255, 0.1)'
  };
  position: relative;
  animation: slideIn 0.3s ease-out;

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

const MessageHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
`;

const SpeakerInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
`;

const SpeakerIcon = styled.div<{ type: 'user' | 'ai' }>`
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  background: ${props => props.type === 'user' ? '#e94560' : '#4ade80'};
  color: #ffffff;
`;

const SpeakerName = styled.span`
  font-weight: 600;
  color: #ffffff;
  font-size: 14px;
`;

const Timestamp = styled.span`
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
`;

const MessageContent = styled.div`
  color: #ffffff;
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
`;

const EmptyState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
`;

const EmptyIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 16px;
  opacity: 0.3;
`;

const EmptyText = styled.p`
  font-size: 16px;
  margin: 0;
  max-width: 300px;
`;

const DiscussionInfo = styled.div`
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 16px;
`;

const InfoRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;

  &:last-child {
    margin-bottom: 0;
  }
`;

const InfoLabel = styled.span`
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
`;

const InfoValue = styled.span`
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
`;

const AudioIndicator = styled.div<{ isProcessing: boolean }>`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: ${props => props.isProcessing ? 'rgba(74, 222, 128, 0.2)' : 'rgba(160, 160, 160, 0.2)'};
  border: 1px solid ${props => props.isProcessing ? '#4ade80' : '#a0a0a0'};
  border-radius: 20px;
  color: ${props => props.isProcessing ? '#4ade80' : '#a0a0a0'};
  font-size: 12px;
  font-weight: 500;
`;

const ProcessingDot = styled.div<{ isProcessing: boolean }>`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${props => props.isProcessing ? '#4ade80' : '#a0a0a0'};
  animation: ${props => props.isProcessing ? 'pulse 1.5s infinite' : 'none'};

  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.3; }
    100% { opacity: 1; }
  }
`;

interface DiscussionPanelProps {
  discussion: DiscussionState;
  audioState: AudioState;
}

const DiscussionPanel: React.FC<DiscussionPanelProps> = ({ discussion, audioState }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [discussion.messages]);

  const formatTimestamp = (timestamp: Date) => {
    return timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getCharacterColor = (characterId?: string) => {
    if (!characterId) return '#4ade80';
    
    const character = discussion.activeCharacters.includes(characterId) 
      ? CHARACTERS.find(c => c.id === characterId)
      : null;
    
    return character?.color || '#4ade80';
  };

  return (
    <Panel>
      <PanelHeader>
        <PanelTitle>
          💭 Live Discussion
          {discussion.isActive && <DiscussionStatus isActive={true}>Active</DiscussionStatus>}
        </PanelTitle>
        
        <AudioIndicator isProcessing={audioState.isProcessing}>
          <ProcessingDot isProcessing={audioState.isProcessing} />
          {audioState.isProcessing ? 'Processing Audio...' : 'Audio Ready'}
        </AudioIndicator>
      </PanelHeader>

      {/* Discussion Info */}
      <DiscussionInfo>
        <InfoRow>
          <InfoLabel>Topic:</InfoLabel>
          <InfoValue>{discussion.topic}</InfoValue>
        </InfoRow>
        <InfoRow>
          <InfoLabel>Active Characters:</InfoLabel>
          <InfoValue>{discussion.activeCharacters.length}</InfoValue>
        </InfoRow>
        <InfoRow>
          <InfoLabel>Current Speaker:</InfoLabel>
          <InfoValue>{discussion.currentSpeaker || 'None'}</InfoValue>
        </InfoRow>
        <InfoRow>
          <InfoLabel>Messages:</InfoLabel>
          <InfoValue>{discussion.messages.length}</InfoValue>
        </InfoRow>
      </DiscussionInfo>

      {/* Messages */}
      <MessagesContainer>
        {discussion.messages.length === 0 ? (
          <EmptyState>
            <EmptyIcon>💭</EmptyIcon>
            <EmptyText>
              No messages yet. Start a discussion to see AI characters in action!
            </EmptyText>
          </EmptyState>
        ) : (
          discussion.messages.map((message) => (
            <Message key={message.id} type={message.type}>
              <MessageHeader>
                <SpeakerInfo>
                  <SpeakerIcon type={message.type}>
                    {message.type === 'user' ? '👤' : '🤖'}
                  </SpeakerIcon>
                  <SpeakerName>{message.speaker}</SpeakerName>
                </SpeakerInfo>
                <Timestamp>{formatTimestamp(message.timestamp)}</Timestamp>
              </MessageHeader>
              <MessageContent>{message.message}</MessageContent>
            </Message>
          ))
        )}
        <div ref={messagesEndRef} />
      </MessagesContainer>
    </Panel>
  );
};

export default DiscussionPanel;