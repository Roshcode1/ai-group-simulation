# 🎤 Voice Discussion Simulator - React App

A modern, real-time AI-powered group discussion simulator built with React, TypeScript, and ElevenLabs API. Features three distinct AI characters with unique personalities and voices, engaging in natural conversations about user-specified topics.

## ✨ Features

### 🎭 **AI Characters**
- **Alex**: Optimistic leader using voice ID `EXAVITQu4vr4xnSDxMaL`
- **Jordan**: Skeptical analyst using voice ID `MF3mGyEYCl7XYWbV9V6O`
- **Taylor**: Creative visionary using voice ID `21m00Tcm4TlvDq8ikWAM`

### 🎤 **Voice Interaction**
- **Speech Recognition**: Real-time voice input via microphone
- **Text-to-Speech**: AI responses using ElevenLabs voices
- **User TTS**: Convert your text messages to speech
- **Voice Recording**: Record and send voice messages

### 🎨 **Modern UI**
- **Responsive Design**: Beautiful, modern interface
- **Dark Theme**: Professional dark color scheme
- **Real-time Updates**: Live discussion display
- **Smooth Animations**: Engaging user experience

### 🔧 **Technical Features**
- **TypeScript**: Full type safety
- **Styled Components**: Modern CSS-in-JS
- **Real-time Audio**: Low-latency voice processing
- **API Integration**: ElevenLabs text-to-speech
- **State Management**: React hooks for state

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Modern web browser with microphone support
- ElevenLabs API key (pre-configured)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd voice-discussion-simulator

# Install dependencies
npm install

# Start development server
npm start
```

### Build for Production
```bash
npm run build
```

## 🎮 How to Use

### 1. **Launch the Application**
- Run `npm start` to open in development mode
- The app will open at `http://localhost:3000`

### 2. **Configure Discussion**
- **API Key**: Your ElevenLabs API key is pre-configured
- **Test Connection**: Click "🧪 Test Connection" to verify API
- **Set Topic**: Enter your discussion topic
- **Select Characters**: Choose which AI characters to include

### 3. **Start Discussion**
- Click "🚀 Start Discussion" to begin
- AI characters will start conversing automatically
- Each character speaks with their unique voice

### 4. **Participate in Discussion**
- **Type & Send**: Enter text and click "📤 Send"
- **Type & Speak**: Enter text and click "🔊 Speak" (TTS)
- **Voice Record**: Click "🎤 Record Voice" and speak

### 5. **Save Discussion**
- Click "💾 Export Discussion" to save as JSON
- Includes all messages, timestamps, and metadata

## 🏗️ Project Structure

```
src/
├── components/           # React components
│   ├── Header.tsx       # Application header
│   ├── ConfigurationPanel.tsx  # Left panel controls
│   └── DiscussionPanel.tsx     # Right panel discussion
├── services/            # API and audio services
│   ├── elevenLabsApi.ts # ElevenLabs API integration
│   └── audioService.ts  # Speech recognition & playback
├── types/               # TypeScript type definitions
│   └── index.ts         # All interfaces and types
├── constants/           # Application constants
│   └── characters.ts    # Character definitions
├── App.tsx              # Main application component
└── index.tsx            # Application entry point
```

## 🔧 Configuration

### Character Settings
Characters are defined in `src/constants/characters.ts`:

```typescript
export const CHARACTERS: Character[] = [
  {
    id: 'alex',
    name: 'Alex',
    voiceId: 'EXAVITQu4vr4xnSDxMaL',
    personality: 'Optimistic Leader',
    description: 'A charismatic and optimistic leader...',
    color: '#4ade80'
  }
  // ... more characters
];
```

### API Configuration
The ElevenLabs API is pre-configured with your key:

```typescript
const [apiConfig, setApiConfig] = useState<ApiConfig>({
  apiKey: 'sk_ec83da917ad8649bc0b92a5cfc65d14e126199c71d0204ad',
  baseUrl: 'https://api.elevenlabs.io/v1',
  isConnected: false
});
```

### Audio Settings
Audio parameters can be adjusted in `src/constants/characters.ts`:

```typescript
export const AUDIO_CONFIG = {
  timeout: 10000,        // 10 seconds
  phraseTimeLimit: 15000, // 15 seconds
  continuous: false
};
```

## 🎨 UI Components

### Header
- Application title and logo
- API connection status
- Version information

### Configuration Panel (Left)
- API configuration and testing
- Discussion topic input
- Character selection checkboxes
- Control buttons (Start/Stop)
- User input methods
- Save/export functionality

### Discussion Panel (Right)
- Live discussion display
- Message history with timestamps
- Speaker identification
- Audio processing indicators
- Discussion statistics

## 🔌 API Integration

### ElevenLabs API
- **Text-to-Speech**: Generate AI character voices
- **Voice Management**: Access to character voice IDs
- **Streaming**: Real-time audio generation
- **Error Handling**: Comprehensive error management

### Speech Recognition
- **Web Speech API**: Browser-native speech recognition
- **Real-time Processing**: Instant voice-to-text conversion
- **Error Handling**: Graceful fallbacks for unsupported browsers

## 🎵 Audio Features

### Speech Recognition
- Automatic microphone detection
- Ambient noise adjustment
- Configurable timeouts and limits
- Error handling for various scenarios

### Text-to-Speech
- High-quality ElevenLabs voices
- Character-specific voice selection
- Streaming audio playback
- Background processing

### Audio Playback
- Web Audio API integration
- Non-blocking audio processing
- Automatic cleanup and memory management
- Cross-browser compatibility

## 🚨 Troubleshooting

### Common Issues

#### **Microphone Not Working**
- Check browser permissions for microphone access
- Ensure microphone is connected and enabled
- Try refreshing the page and granting permissions again

#### **Speech Recognition Issues**
- Ensure you're using a modern browser (Chrome, Firefox, Safari)
- Check internet connection (required for Google Speech Recognition)
- Speak clearly and reduce background noise

#### **API Connection Errors**
- Verify your ElevenLabs API key is valid
- Check account has sufficient credits
- Ensure you're not hitting rate limits

#### **Audio Playback Issues**
- Check system audio settings
- Ensure speakers/headphones are connected
- Try refreshing the page

### Browser Compatibility
- **Chrome**: Full support for all features
- **Firefox**: Full support for all features
- **Safari**: Full support for all features
- **Edge**: Full support for all features

## 🔮 Future Enhancements

### Planned Features
- **Custom AI Models**: Integration with other AI services
- **Voice Cloning**: Custom voice training capabilities
- **Discussion Templates**: Pre-defined conversation structures
- **Multi-language Support**: International language support
- **Collaboration**: Multi-user discussion sessions

### Technical Improvements
- **WebRTC**: Enhanced audio streaming
- **WebSocket**: Real-time collaboration
- **PWA**: Progressive web app capabilities
- **Offline Support**: Cached responses and offline mode

## 📚 Development

### Available Scripts
```bash
npm start          # Start development server
npm run build      # Build for production
npm test           # Run test suite
npm run eject      # Eject from Create React App
```

### Dependencies
- **React 18**: Modern React with hooks
- **TypeScript**: Type safety and better development experience
- **Styled Components**: CSS-in-JS styling
- **Axios**: HTTP client for API calls
- **Web APIs**: Native browser APIs for audio

### Development Guidelines
- Use TypeScript for all new code
- Follow React functional component patterns
- Use styled-components for styling
- Implement proper error handling
- Add TypeScript interfaces for all data structures

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🆘 Support

For issues and questions:
- Check the troubleshooting section above
- Review ElevenLabs documentation
- Open an issue in the repository

## 🙏 Acknowledgments

- [ElevenLabs](https://elevenlabs.io) for their excellent TTS API
- [React](https://reactjs.org) for the amazing framework
- [Styled Components](https://styled-components.com) for styling
- [TypeScript](https://www.typescriptlang.org) for type safety

---

**🎤 Your React Voice Discussion Simulator is ready to create amazing AI-powered conversations!**