import React from 'react';
import styled from 'styled-components';

const HeaderContainer = styled.header`
  background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  border-bottom: 2px solid #e94560;
`;

const HeaderContent = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const LogoSection = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
`;

const Logo = styled.div`
  font-size: 2.5rem;
  font-weight: bold;
  background: linear-gradient(45deg, #e94560, #4ade80);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const Title = styled.h1`
  font-size: 2rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
`;

const Subtitle = styled.p`
  color: #a0a0a0;
  margin: 0;
  font-size: 1rem;
`;

const StatusSection = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
`;

const StatusIndicator = styled.div<{ isOnline: boolean }>`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: ${props => props.isOnline ? 'rgba(74, 222, 128, 0.2)' : 'rgba(248, 113, 113, 0.2)'};
  border: 1px solid ${props => props.isOnline ? '#4ade80' : '#f87171'};
  border-radius: 20px;
  color: ${props => props.isOnline ? '#4ade80' : '#f87171'};
  font-size: 0.9rem;
  font-weight: 500;
`;

const StatusDot = styled.div<{ isOnline: boolean }>`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${props => props.isOnline ? '#4ade80' : '#f87171'};
  animation: ${props => props.isOnline ? 'pulse 2s infinite' : 'none'};

  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
  }
`;

const Version = styled.div`
  color: #a0a0a0;
  font-size: 0.8rem;
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
`;

const Header: React.FC = () => {
  return (
    <HeaderContainer>
      <HeaderContent>
        <LogoSection>
          <Logo>🎤</Logo>
          <div>
            <Title>Voice Discussion Simulator</Title>
            <Subtitle>AI-Powered Group Discussions with Real-Time Voice Interaction</Subtitle>
          </div>
        </LogoSection>
        
        <StatusSection>
          <StatusIndicator isOnline={true}>
            <StatusDot isOnline={true} />
            API Connected
          </StatusIndicator>
          <Version>v1.0.0</Version>
        </StatusSection>
      </HeaderContent>
    </HeaderContainer>
  );
};

export default Header;