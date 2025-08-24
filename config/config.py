"""
Configuration file for the Voice Discussion Simulator
"""

# ElevenLabs API Configuration
ELEVENLABS_API_BASE_URL = "https://api.elevenlabs.io/v1"
ELEVENLABS_MODEL = "eleven_monolingual_v1"

# Character Definitions
CHARACTERS = {
    'Alex': {
        'name': 'Alex',
        'voice_id': 'EXAVITQu4vr4xnSDxMaL',
        'personality': 'optimistic leader',
        'description': 'A charismatic and optimistic leader who encourages collaboration and sees opportunities in challenges.',
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.75,
            'style': 0.0,
            'use_speaker_boost': True
        }
    },
    'Jordan': {
        'name': 'Jordan',
        'voice_id': 'MF3mGyEYCl7XYWbV9V6O',
        'personality': 'skeptical analyst',
        'description': 'A critical thinker who analyzes situations carefully and asks probing questions.',
        'voice_settings': {
            'stability': 0.7,
            'similarity_boost': 0.8,
            'style': 0.0,
            'use_speaker_boost': True
        }
    },
    'Taylor': {
        'name': 'Taylor',
        'voice_id': '21m00Tcm4TlvDq8ikWAM',
        'personality': 'creative visionary',
        'description': 'An innovative thinker who brings creative solutions and thinks outside the box.',
        'voice_settings': {
            'stability': 0.6,
            'similarity_boost': 0.7,
            'style': 0.3,
            'use_speaker_boost': True
        }
    }
}

# Audio Configuration
AUDIO_CONFIG = {
    'format': 'pyaudio.paInt16',
    'channels': 1,
    'rate': 44100,
    'chunk': 1024,
    'timeout': 5,
    'phrase_time_limit': 10
}

# Discussion Configuration
DISCUSSION_CONFIG = {
    'max_turns': 20,
    'turn_delay': 2.0,  # seconds
    'response_length': 'short',  # short, medium, long
    'interaction_style': 'natural'  # natural, formal, casual
}

# UI Configuration
UI_CONFIG = {
    'window_size': '800x600',
    'theme': 'default',
    'font_family': 'Arial',
    'font_size': 10,
    'title_font_size': 16
}

# Error Messages
ERROR_MESSAGES = {
    'api_key_missing': 'Please enter your ElevenLabs API key',
    'api_key_invalid': 'Invalid API key. Please check and try again.',
    'topic_missing': 'Please enter a discussion topic',
    'audio_init_failed': 'Failed to initialize audio system',
    'recording_failed': 'Failed to start recording',
    'tts_failed': 'Failed to generate speech',
    'network_error': 'Network error. Please check your connection.',
    'api_limit_reached': 'API rate limit reached. Please wait and try again.'
}

# Success Messages
SUCCESS_MESSAGES = {
    'api_key_valid': 'API key validated successfully',
    'discussion_started': 'Discussion started successfully',
    'recording_started': 'Recording started. Speak now!',
    'recording_stopped': 'Recording stopped',
    'audio_generated': 'Audio generated successfully'
}