import axios from 'axios';
import { ElevenLabsVoice } from '../types';
import { API_CONFIG } from '../constants/characters';

class ElevenLabsApiService {
  private apiKey: string;
  private baseUrl: string;

  constructor(apiKey: string) {
    this.apiKey = apiKey;
    this.baseUrl = API_CONFIG.baseUrl;
  }

  private getHeaders() {
    return {
      'xi-api-key': this.apiKey,
      'Content-Type': 'application/json'
    };
  }

  async testConnection(): Promise<boolean> {
    try {
      const response = await axios.get(`${this.baseUrl}/voices`, {
        headers: this.getHeaders()
      });
      return response.status === 200;
    } catch (error) {
      console.error('API connection test failed:', error);
      return false;
    }
  }

  async getVoices(): Promise<ElevenLabsVoice[]> {
    try {
      const response = await axios.get(`${this.baseUrl}/voices`, {
        headers: this.getHeaders()
      });
      return response.data.voices || [];
    } catch (error) {
      console.error('Failed to fetch voices:', error);
      throw new Error('Failed to fetch voices');
    }
  }

  async generateSpeech(text: string, voiceId: string): Promise<ArrayBuffer> {
    try {
      const response = await axios.post(
        `${this.baseUrl}/text-to-speech/${voiceId}`,
        {
          text,
          model_id: API_CONFIG.model,
          voice_settings: {
            stability: 0.7,
            similarity_boost: 0.8,
            style: 0.0,
            use_speaker_boost: true
          }
        },
        {
          headers: this.getHeaders(),
          responseType: 'arraybuffer'
        }
      );
      return response.data;
    } catch (error) {
      console.error('Failed to generate speech:', error);
      throw new Error('Failed to generate speech');
    }
  }

  async generateSpeechStream(text: string, voiceId: string): Promise<ReadableStream> {
    try {
      const response = await fetch(`${this.baseUrl}/text-to-speech/${voiceId}/stream`, {
        method: 'POST',
        headers: {
          'xi-api-key': this.apiKey,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          text,
          model_id: API_CONFIG.model,
          voice_settings: {
            stability: 0.7,
            similarity_boost: 0.8,
            style: 0.0,
            use_speaker_boost: true
          }
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return response.body!;
    } catch (error) {
      console.error('Failed to generate speech stream:', error);
      throw new Error('Failed to generate speech stream');
    }
  }

  async cloneVoice(name: string, files: File[]): Promise<string> {
    try {
      const formData = new FormData();
      formData.append('name', name);
      
      files.forEach((file, index) => {
        formData.append(`files`, file);
      });

      const response = await axios.post(`${this.baseUrl}/voices/add`, formData, {
        headers: {
          'xi-api-key': this.apiKey
        }
      });

      return response.data.voice_id;
    } catch (error) {
      console.error('Failed to clone voice:', error);
      throw new Error('Failed to clone voice');
    }
  }

  async deleteVoice(voiceId: string): Promise<boolean> {
    try {
      await axios.delete(`${this.baseUrl}/voices/${voiceId}`, {
        headers: this.getHeaders()
      });
      return true;
    } catch (error) {
      console.error('Failed to delete voice:', error);
      return false;
    }
  }
}

export default ElevenLabsApiService;