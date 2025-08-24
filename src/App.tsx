import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import Header from './components/Header';
import ConfigurationPanel from './components/ConfigurationPanel';
import DiscussionPanel from './components/DiscussionPanel';
import { DiscussionState, AudioState, ApiConfig, Character } from './types';
import { CHARACTERS, DEFAULT_TOPIC } from './constants/characters';
import ElevenLabsApiService from './services/elevenLabsApi';
import AudioService from './services/audioService';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: #ffffff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
`;

const MainContent = styled.div`
  display: flex;
  gap: 20px;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  height: calc(100vh - 120px);
`;

const LeftPanel = styled.div`
  width: 400px;
  flex-shrink: 0;
`;

const RightPanel = styled.div`
  flex: 1;
  min-width: 0;
`;

function App() {
  // State management
  const [discussionState, setDiscussionState] = useState<DiscussionState>({
    topic: DEFAULT_TOPIC,
    isActive: false,
    currentSpeaker: null,
    messages: [],
    activeCharacters: CHARACTERS.map(c => c.id)
  });

  const [audioState, setAudioState] = useState<AudioState>({
    isRecording: false,
    isPlaying: false,
    isProcessing: false
  });

  const [apiConfig, setApiConfig] = useState<ApiConfig>({
    apiKey: 'sk_ec83da917ad8649bc0b92a5cfc65d14e126199c71d0204ad',
    baseUrl: 'https://api.elevenlabs.io/v1',
    isConnected: false
  });

  // Services
  const [elevenLabsApi, setElevenLabsApi] = useState<ElevenLabsApiService | null>(null);
  const [audioService, setAudioService] = useState<AudioService | null>(null);

  // Initialize services
  useEffect(() => {
    const api = new ElevenLabsApiService(apiConfig.apiKey);
    const audio = new AudioService();
    
    setElevenLabsApi(api);
    setAudioService(audio);

    // Test API connection on startup
    testApiConnection(api);
  }, []);

  const testApiConnection = async (api: ElevenLabsApiService) => {
    try {
      const isConnected = await api.testConnection();
      setApiConfig(prev => ({ ...prev, isConnected }));
    } catch (error) {
      console.error('API connection test failed:', error);
      setApiConfig(prev => ({ ...prev, isConnected: false }));
    }
  };

  const startDiscussion = () => {
    if (!apiConfig.isConnected) {
      alert('Please test API connection first');
      return;
    }

    setDiscussionState(prev => ({ ...prev, isActive: true }));
    
    // Start AI discussion
    startAIDiscussion();
  };

  const stopDiscussion = () => {
    setDiscussionState(prev => ({ ...prev, isActive: false }));
    setAudioState(prev => ({ ...prev, isRecording: false }));
  };

  const startAIDiscussion = async () => {
    if (!elevenLabsApi || !discussionState.activeCharacters.length) return;

    const activeChars = CHARACTERS.filter(c => 
      discussionState.activeCharacters.includes(c.id)
    );

    // Start with first character
    let currentCharIndex = 0;
    let turnCount = 0;
    const maxTurns = 10;

    const continueDiscussion = async () => {
      if (!discussionState.isActive || turnCount >= maxTurns) return;

      const currentChar = activeChars[currentCharIndex];
      const response = generateAIResponse(currentChar);
      
      // Add AI message
      const aiMessage = {
        id: Date.now().toString(),
        speaker: currentChar.name,
        message: response,
        timestamp: new Date(),
        type: 'ai' as const,
        characterId: currentChar.id
      };

      setDiscussionState(prev => ({
        ...prev,
        messages: [...prev.messages, aiMessage],
        currentSpeaker: currentChar.name
      }));

      // Play AI response
      try {
        setAudioState(prev => ({ ...prev, isProcessing: true }));
        const audioBuffer = await elevenLabsApi.generateSpeech(response, currentChar.voiceId);
        await audioService?.playAudio(audioBuffer);
        setAudioState(prev => ({ ...prev, isProcessing: false }));
      } catch (error) {
        console.error('Failed to play AI response:', error);
        setAudioState(prev => ({ ...prev, isProcessing: false }));
      }

      // Switch to next character
      currentCharIndex = (currentCharIndex + 1) % activeChars.length;
      turnCount++;

      // Continue after delay
      setTimeout(continueDiscussion, 3000);
    };

    // Start the discussion
    continueDiscussion();
  };

  const generateAIResponse = (character: Character): string => {
    const responses = {
      alex: [
        "I think this is a fantastic opportunity for us to explore new possibilities.",
        "Let's focus on the positive aspects and how we can make this work together.",
        "I'm excited about the potential here - we just need to take that first step.",
        "This could really transform how we approach the entire field.",
        "I believe we're on the right track with this direction."
      ],
      jordan: [
        "That's an interesting point, but I have some concerns we should address.",
        "We need to carefully consider the implications before moving forward.",
        "I'd like to understand the risks involved in this approach.",
        "Let me play devil's advocate here for a moment.",
        "We should examine the data more carefully before making decisions."
      ],
      taylor: [
        "What if we approached this from a completely different angle?",
        "I'm thinking outside the box here - maybe we need a paradigm shift.",
        "Let's get creative and explore some unconventional solutions.",
        "This reminds me of a completely different problem we solved last year.",
        "I have a wild idea that might just work."
      ]
    };

    const charResponses = responses[character.id as keyof typeof responses] || responses.alex;
    return charResponses[Math.floor(Math.random() * charResponses.length)];
  };

  const addUserMessage = (message: string, useTTS: boolean = false) => {
    const userMessage = {
      id: Date.now().toString(),
      speaker: 'You',
      message,
      timestamp: new Date(),
      type: 'user' as const
    };

    setDiscussionState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage]
    }));

    // If TTS is enabled, play the user message
    if (useTTS && elevenLabsApi && audioService) {
      playUserTTS(message);
    }

    // Generate AI response
    generateUserResponse(message);
  };

  const playUserTTS = async (text: string) => {
    if (!elevenLabsApi || !audioService) return;

    try {
      setAudioState(prev => ({ ...prev, isProcessing: true }));
      const audioBuffer = await elevenLabsApi.generateSpeech(text, CHARACTERS[0].voiceId);
      await audioService.playAudio(audioBuffer);
      setAudioState(prev => ({ ...prev, isProcessing: false }));
    } catch (error) {
      console.error('Failed to play user TTS:', error);
      setAudioState(prev => ({ ...prev, isProcessing: false }));
    }
  };

  const generateUserResponse = (userInput: string) => {
    if (!discussionState.activeCharacters.length) return;

    const activeChars = CHARACTERS.filter(c => 
      discussionState.activeCharacters.includes(c.id)
    );

    // Select next character to respond
    const currentChar = activeChars[Math.floor(Math.random() * activeChars.length)];
    const response = generateAIResponse(currentChar);

    const aiMessage = {
      id: Date.now().toString(),
      speaker: currentChar.name,
      message: response,
      timestamp: new Date(),
      type: 'ai' as const,
      characterId: currentChar.id
    };

    setDiscussionState(prev => ({
      ...prev,
      messages: [...prev.messages, aiMessage],
      currentSpeaker: currentChar.name
    }));

    // Play AI response
    if (elevenLabsApi && audioService) {
      playAIResponse(response, currentChar.voiceId);
    }
  };

  const playAIResponse = async (text: string, voiceId: string) => {
    if (!elevenLabsApi || !audioService) return;

    try {
      setAudioState(prev => ({ ...prev, isProcessing: true }));
      const audioBuffer = await elevenLabsApi.generateSpeech(text, voiceId);
      await audioService.playAudio(audioBuffer);
      setAudioState(prev => ({ ...prev, isProcessing: false }));
    } catch (error) {
      console.error('Failed to play AI response:', error);
      setAudioState(prev => ({ ...prev, isProcessing: false }));
    }
  };

  const handleCharacterToggle = (characterId: string, isActive: boolean) => {
    setDiscussionState(prev => ({
      ...prev,
      activeCharacters: isActive 
        ? [...prev.activeCharacters, characterId]
        : prev.activeCharacters.filter(id => id !== characterId)
    }));
  };

  const handleTopicChange = (topic: string) => {
    setDiscussionState(prev => ({ ...prev, topic }));
  };

  const handleVoiceRecording = async () => {
    if (!audioService) return;

    if (audioState.isRecording) {
      setAudioState(prev => ({ ...prev, isRecording: false }));
      audioService.stopListening();
    } else {
      setAudioState(prev => ({ ...prev, isRecording: true }));
      
      audioService.startListening(
        (text) => {
          addUserMessage(text);
          setAudioState(prev => ({ ...prev, isRecording: false }));
        },
        (error) => {
          alert(`Speech recognition error: ${error}`);
          setAudioState(prev => ({ ...prev, isRecording: false }));
        }
      );
    }
  };

  const saveDiscussion = () => {
    const discussionData = {
      topic: discussionState.topic,
      timestamp: new Date().toISOString(),
      messages: discussionState.messages
    };

    const blob = new Blob([JSON.stringify(discussionData, null, 2)], {
      type: 'application/json'
    });

    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `discussion-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <AppContainer>
      <Header />
      <MainContent>
        <LeftPanel>
          <ConfigurationPanel
            topic={discussionState.topic}
            onTopicChange={handleTopicChange}
            characters={CHARACTERS}
            activeCharacters={discussionState.activeCharacters}
            onCharacterToggle={handleCharacterToggle}
            isDiscussionActive={discussionState.isActive}
            onStartDiscussion={startDiscussion}
            onStopDiscussion={stopDiscussion}
            onSaveDiscussion={saveDiscussion}
            apiConfig={apiConfig}
            onTestApi={() => elevenLabsApi && testApiConnection(elevenLabsApi)}
            audioState={audioState}
            onVoiceRecording={handleVoiceRecording}
            onAddUserMessage={addUserMessage}
          />
        </LeftPanel>
        <RightPanel>
          <DiscussionPanel
            discussion={discussionState}
            audioState={audioState}
          />
        </RightPanel>
      </MainContent>
    </AppContainer>
  );
}

export default App;