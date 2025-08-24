# Voice-Based Group Discussion Simulator

A real-time AI-powered group discussion simulator that uses the ElevenLabs Conversational AI API to create dynamic, multi-character discussions. The simulator features three distinct AI characters with unique personalities and voices, engaging in natural conversations about user-specified topics.

## Features

- **Multi-Character AI Discussion**: Three AI characters with distinct personalities:
  - **Alex**: Optimistic leader who encourages collaboration
  - **Jordan**: Skeptical analyst who asks probing questions
  - **Taylor**: Creative visionary who thinks outside the box

- **Real-Time Voice Interaction**: 
  - Speech-to-text for user input via microphone
  - Text-to-speech output using ElevenLabs voices
  - Low-latency audio streaming

- **Natural Turn-Taking**: Intelligent conversation flow that mimics real group discussions

- **Customizable Topics**: Users can specify any discussion topic

- **Voice Selection**: Uses specific ElevenLabs voice IDs for each character:
  - Alex: `EXAVITQu4vr4xnSDxMaL`
  - Jordan: `MF3mGyEYCl7XYWbV9V6O`
  - Taylor: `21m00Tcm4TlvDq8ikWAM`

- **Discussion Recording**: Save discussions as text or JSON files

- **Character Configuration**: Enable/disable specific characters for discussions

## Prerequisites

- Python 3.8 or higher
- ElevenLabs API key (get one at [elevenlabs.io](https://elevenlabs.io))
- Microphone and speakers/headphones
- Linux, macOS, or Windows

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd voice-discussion-simulator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: On some systems, you may need to install additional system dependencies:

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install python3-dev portaudio19-dev python3-pyaudio
sudo apt-get install libasound2-dev
```

#### macOS:
```bash
brew install portaudio
```

#### Windows:
PyAudio should install automatically with pip.

### 3. Get Your ElevenLabs API Key

1. Visit [elevenlabs.io](https://elevenlabs.io)
2. Create an account and log in
3. Navigate to your profile settings
4. Copy your API key

## Usage

### 1. Launch the Application

```bash
python src/enhanced_simulator.py
```

### 2. Configure the Application

1. **Enter API Key**: Paste your ElevenLabs API key in the designated field
2. **Test Connection**: Click "Test API Connection" to verify your key works
3. **Set Topic**: Enter the discussion topic (default: "The future of artificial intelligence in education")
4. **Select Characters**: Choose which AI characters to include in the discussion

### 3. Start the Discussion

1. Click "Start Discussion" to begin
2. The AI characters will start discussing the topic automatically
3. Use the "🎤 Record" button to add your voice input
4. Click "Stop Discussion" to end the session

### 4. Save Discussions

- Click "💾 Save Discussion" to save the conversation
- Choose between text (.txt) or JSON (.json) format
- Discussions include timestamps and speaker information

## Configuration

### Character Personalities

You can modify character personalities and voice settings in `config/config.py`:

```python
CHARACTERS = {
    'Alex': {
        'name': 'Alex',
        'voice_id': 'EXAVITQu4vr4xnSDxMaL',
        'personality': 'optimistic leader',
        'description': 'A charismatic and optimistic leader...',
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.75,
            'style': 0.0,
            'use_speaker_boost': True
        }
    }
    # ... other characters
}
```

### Audio Settings

Adjust audio parameters in the configuration:

```python
AUDIO_CONFIG = {
    'format': 'pyaudio.paInt16',
    'channels': 1,
    'rate': 44100,
    'chunk': 1024,
    'timeout': 5,
    'phrase_time_limit': 10
}
```

### Discussion Parameters

```python
DISCUSSION_CONFIG = {
    'max_turns': 20,
    'turn_delay': 2.0,  # seconds between turns
    'response_length': 'short',
    'interaction_style': 'natural'
}
```

## Troubleshooting

### Common Issues

#### Audio Not Working
- Ensure your microphone is properly connected and enabled
- Check system audio permissions
- Try running with `python -m pip install --upgrade pyaudio`

#### API Key Errors
- Verify your ElevenLabs API key is correct
- Check your account has sufficient credits
- Ensure you're not hitting rate limits

#### PyAudio Installation Issues
- On Linux: Install system dependencies first
- On macOS: Use `brew install portaudio`
- On Windows: Try `pip install pipwin` then `pipwin install pyaudio`

#### Speech Recognition Issues
- Ensure good microphone quality
- Reduce background noise
- Check internet connection (Google Speech Recognition requires it)

### Error Messages

- **"No audio devices found"**: Check microphone connection and system settings
- **"API rate limit reached"**: Wait before making more requests or upgrade your plan
- **"Could not understand speech"**: Speak more clearly or check microphone quality

## API Usage and Costs

The application uses the ElevenLabs API for:
- Text-to-speech generation
- Voice cloning and management

**Costs**: ElevenLabs offers free tier with limited usage. Check [their pricing](https://elevenlabs.io/pricing) for current rates.

**Rate Limits**: Free tier has monthly character limits. Monitor usage in your ElevenLabs dashboard.

## Development

### Project Structure

```
voice-discussion-simulator/
├── src/
│   ├── main.py                 # Basic simulator
│   └── enhanced_simulator.py   # Enhanced version with better UI
├── config/
│   └── config.py               # Configuration and constants
├── audio/                      # Audio file storage (if needed)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

### Adding New Characters

1. Add character definition to `config/config.py`
2. Include voice ID from ElevenLabs
3. Define personality and response patterns
4. Update the UI to include the new character

### Extending Functionality

- **Custom AI Models**: Integrate with other AI services
- **Voice Cloning**: Add custom voice training capabilities
- **Discussion Analytics**: Track conversation patterns and insights
- **Multi-Language Support**: Add support for different languages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review ElevenLabs documentation
- Open an issue in the repository

## Acknowledgments

- [ElevenLabs](https://elevenlabs.io) for their excellent TTS API
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) for audio I/O
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) for STT capabilities

---

**Note**: This is a demonstration application. For production use, consider implementing proper error handling, logging, and security measures.