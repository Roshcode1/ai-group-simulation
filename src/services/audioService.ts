class AudioService {
  private recognition: any;
  private isSupported: boolean;

  constructor() {
    this.isSupported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
    
    if (this.isSupported) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      this.recognition = new SpeechRecognition();
      this.setupRecognition();
    }
  }

  private setupRecognition() {
    if (!this.recognition) return;

    this.recognition.continuous = false;
    this.recognition.interimResults = false;
    this.recognition.lang = 'en-US';
    this.recognition.maxAlternatives = 1;
  }

  isSpeechRecognitionSupported(): boolean {
    return this.isSupported;
  }

  startListening(onResult: (text: string) => void, onError: (error: string) => void): void {
    if (!this.recognition) {
      onError('Speech recognition not supported');
      return;
    }

    this.recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      onResult(transcript);
    };

    this.recognition.onerror = (event: any) => {
      let errorMessage = 'Speech recognition error';
      
      switch (event.error) {
        case 'no-speech':
          errorMessage = 'No speech detected';
          break;
        case 'audio-capture':
          errorMessage = 'Audio capture failed';
          break;
        case 'not-allowed':
          errorMessage = 'Microphone access denied';
          break;
        case 'network':
          errorMessage = 'Network error';
          break;
        default:
          errorMessage = `Speech recognition error: ${event.error}`;
      }
      
      onError(errorMessage);
    };

    this.recognition.onend = () => {
      // Recognition ended
    };

    try {
      this.recognition.start();
    } catch (error) {
      onError('Failed to start speech recognition');
    }
  }

  stopListening(): void {
    if (this.recognition) {
      this.recognition.stop();
    }
  }

  async playAudio(audioBuffer: ArrayBuffer): Promise<void> {
    try {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const audioSource = audioContext.createBufferSource();
      
      const arrayBuffer = audioBuffer;
      const audioBuffer2 = await audioContext.decodeAudioData(arrayBuffer);
      
      audioSource.buffer = audioBuffer2;
      audioSource.connect(audioContext.destination);
      audioSource.start(0);
      
      return new Promise((resolve) => {
        audioSource.onended = () => resolve();
      });
    } catch (error) {
      console.error('Error playing audio:', error);
      throw new Error('Failed to play audio');
    }
  }

  async playAudioStream(stream: ReadableStream): Promise<void> {
    try {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const reader = stream.getReader();
      
      const chunks: Uint8Array[] = [];
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        chunks.push(value);
      }
      
      const audioData = new Uint8Array(chunks.reduce((acc, chunk) => acc + chunk.length, 0));
      let offset = 0;
      
      for (const chunk of chunks) {
        audioData.set(chunk, offset);
        offset += chunk.length;
      }
      
      const audioBuffer = await audioContext.decodeAudioData(audioData.buffer);
      const audioSource = audioContext.createBufferSource();
      
      audioSource.buffer = audioBuffer;
      audioSource.connect(audioContext.destination);
      audioSource.start(0);
      
      return new Promise((resolve) => {
        audioSource.onended = () => resolve();
      });
    } catch (error) {
      console.error('Error playing audio stream:', error);
      throw new Error('Failed to play audio stream');
    }
  }

  async recordAudio(duration: number = 5000): Promise<Blob> {
    return new Promise((resolve, reject) => {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        reject(new Error('Media devices not supported'));
        return;
      }

      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          const mediaRecorder = new MediaRecorder(stream);
          const chunks: Blob[] = [];

          mediaRecorder.ondataavailable = (event) => {
            chunks.push(event.data);
          };

          mediaRecorder.onstop = () => {
            const blob = new Blob(chunks, { type: 'audio/wav' });
            stream.getTracks().forEach(track => track.stop());
            resolve(blob);
          };

          mediaRecorder.start();
          
          setTimeout(() => {
            mediaRecorder.stop();
          }, duration);
        })
        .catch(error => {
          reject(error);
        });
    });
  }

  getAudioDevices(): Promise<MediaDeviceInfo[]> {
    return navigator.mediaDevices.enumerateDevices()
      .then(devices => devices.filter(device => device.kind === 'audioinput'));
  }
}

export default AudioService;