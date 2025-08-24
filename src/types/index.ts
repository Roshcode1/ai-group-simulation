export interface Character {
  id: string;
  name: string;
  voiceId: string;
  personality: string;
  description: string;
  color: string;
}

export interface DiscussionMessage {
  id: string;
  speaker: string;
  message: string;
  timestamp: Date;
  type: 'user' | 'ai';
  characterId?: string;
}

export interface DiscussionState {
  topic: string;
  isActive: boolean;
  currentSpeaker: string | null;
  messages: DiscussionMessage[];
  activeCharacters: string[];
}

export interface AudioState {
  isRecording: boolean;
  isPlaying: boolean;
  isProcessing: boolean;
}

export interface ApiConfig {
  apiKey: string;
  baseUrl: string;
  isConnected: boolean;
}

export interface UserInput {
  text: string;
  useTTS: boolean;
}

export interface ElevenLabsVoice {
  voice_id: string;
  name: string;
  category: string;
  available_for_tiers: string[];
  settings: {
    stability: number;
    similarity_boost: number;
    style: number;
    use_speaker_boost: boolean;
  };
}