import { Character } from '../types';

export const CHARACTERS: Character[] = [
  {
    id: 'alex',
    name: 'Alex',
    voiceId: 'EXAVITQu4vr4xnSDxMaL',
    personality: 'Optimistic Leader',
    description: 'A charismatic and optimistic leader who encourages collaboration and sees opportunities in challenges.',
    color: '#4ade80'
  },
  {
    id: 'jordan',
    name: 'Jordan',
    voiceId: 'MF3mGyEYCl7XYWbV9V6O',
    personality: 'Skeptical Analyst',
    description: 'A critical thinker who analyzes situations carefully and asks probing questions.',
    color: '#fbbf24'
  },
  {
    id: 'taylor',
    name: 'Taylor',
    voiceId: '21m00Tcm4TlvDq8ikWAM',
    personality: 'Creative Visionary',
    description: 'An innovative thinker who brings creative solutions and thinks outside the box.',
    color: '#e94560'
  }
];

export const DEFAULT_TOPIC = 'The future of artificial intelligence in education';

export const API_CONFIG = {
  baseUrl: 'https://api.elevenlabs.io/v1',
  model: 'eleven_monolingual_v1'
};

export const AUDIO_CONFIG = {
  timeout: 10000,
  phraseTimeLimit: 15000,
  continuous: false
};

export const DISCUSSION_CONFIG = {
  maxTurns: 20,
  turnDelay: 2000,
  responseLength: 'short'
};