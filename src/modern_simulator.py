#!/usr/bin/env python3
"""
Modern Voice Discussion Simulator
A real-time AI-powered group discussion simulator with modern UI and fixed audio recording
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import queue
import time
import os
import json
import sys
from typing import Dict, List, Optional, Tuple
import speech_recognition as sr
import sounddevice as sd
import numpy as np
from elevenlabs import generate, stream, set_api_key, Voice, VoiceSettings, voices
from elevenlabs.api import History
import tempfile
import wave
import pyaudio
import requests
from pathlib import Path
import queue

# Add config directory to path
sys.path.append(str(Path(__file__).parent.parent / 'config'))
from config import CHARACTERS, AUDIO_CONFIG, DISCUSSION_CONFIG, UI_CONFIG, ERROR_MESSAGES, SUCCESS_MESSAGES

class ModernVoiceDiscussionSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎤 Modern Voice Discussion Simulator")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')
        
        # Set API key
        self.api_key = "sk_ec83da917ad8649bc0b92a5cfc65d14e126199c71d0204ad"
        set_api_key(self.api_key)
        
        # Audio configuration
        self.audio_format = getattr(pyaudio, AUDIO_CONFIG['format'].split('.')[-1])
        self.channels = AUDIO_CONFIG['channels']
        self.rate = AUDIO_CONFIG['rate']
        self.chunk = AUDIO_CONFIG['chunk']
        self.recording = False
        self.playing = False
        
        # Character definitions
        self.characters = CHARACTERS.copy()
        
        # Discussion state
        self.topic = ""
        self.discussion_history = []
        self.current_speaker = None
        self.discussion_active = False
        
        # Audio components
        self.audio = None
        self.recognizer = sr.Recognizer()
        self.microphone = None
        
        # Audio recording queue
        self.audio_queue = queue.Queue()
        
        # Initialize components
        self.initialize_audio()
        self.setup_modern_ui()
        
    def initialize_audio(self):
        """Initialize audio components with error handling"""
        try:
            self.audio = pyaudio.PyAudio()
            
            # Check available microphones
            info = self.audio.get_host_api_info_by_index(0)
            numdevices = info.get('deviceCount')
            
            if numdevices == 0:
                raise Exception("No audio devices found")
            
            # Find default microphone
            for i in range(numdevices):
                device_info = self.audio.get_device_info_by_host_api_device_index(0, i)
                if device_info.get('maxInputChannels') > 0:
                    self.microphone = sr.Microphone(device_index=i)
                    break
            else:
                self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
        except Exception as e:
            messagebox.showerror("Audio Error", f"Failed to initialize audio: {str(e)}")
            self.microphone = None
    
    def setup_modern_ui(self):
        """Initialize the modern user interface"""
        # Configure modern style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom colors
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#e94560',
            'text_light': '#ffffff',
            'text_dark': '#1a1a2e',
            'success': '#4ade80',
            'warning': '#fbbf24',
            'error': '#f87171'
        }
        
        # Configure custom styles
        style.configure('Modern.TFrame', background=self.colors['bg_dark'])
        style.configure('Modern.TLabel', background=self.colors['bg_dark'], foreground=self.colors['text_light'])
        style.configure('Modern.TButton', 
                       background=self.colors['accent'], 
                       foreground=self.colors['text_light'],
                       borderwidth=0,
                       focuscolor='none')
        style.map('Modern.TButton',
                 background=[('active', self.colors['bg_light']),
                           ('pressed', self.colors['bg_medium'])])
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Left panel - Configuration
        left_panel = self.create_left_panel(content_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Right panel - Discussion
        right_panel = self.create_right_panel(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def create_header(self, parent):
        """Create modern header"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_medium'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="🎤 Modern Voice Discussion Simulator",
                              font=('Helvetica', 24, 'bold'),
                              bg=self.colors['bg_medium'],
                              fg=self.colors['text_light'])
        title_label.pack(expand=True)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="AI-Powered Group Discussions with Real-Time Voice Interaction",
                                 font=('Helvetica', 12),
                                 bg=self.colors['bg_medium'],
                                 fg=self.colors['accent'])
        subtitle_label.pack()
        
    def create_left_panel(self, parent):
        """Create left configuration panel"""
        left_frame = tk.Frame(parent, bg=self.colors['bg_medium'], width=350)
        left_frame.pack_propagate(False)
        
        # API Status
        api_frame = self.create_section_frame(left_frame, "🔑 API Configuration", self.colors['bg_light'])
        api_frame.pack(fill=tk.X, pady=(0, 15))
        
        # API key display (masked)
        api_key_display = f"sk_...{self.api_key[-8:]}"
        api_label = tk.Label(api_frame, 
                            text=f"API Key: {api_key_display}",
                            bg=self.colors['bg_light'],
                            fg=self.colors['text_light'],
                            font=('Courier', 10))
        api_label.pack(pady=10)
        
        # Test API button
        test_api_button = tk.Button(api_frame,
                                   text="🧪 Test API Connection",
                                   command=self.test_api_connection,
                                   bg=self.colors['accent'],
                                   fg=self.colors['text_light'],
                                   font=('Helvetica', 12, 'bold'),
                                   relief=tk.FLAT,
                                   padx=20,
                                   pady=10)
        test_api_button.pack(pady=(0, 10))
        
        # Topic Configuration
        topic_frame = self.create_section_frame(left_frame, "📝 Discussion Topic", self.colors['bg_light'])
        topic_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.topic_entry = tk.Entry(topic_frame,
                                   font=('Helvetica', 12),
                                   bg=self.colors['bg_dark'],
                                   fg=self.colors['text_light'],
                                   insertbackground=self.colors['accent'])
        self.topic_entry.pack(fill=tk.X, padx=15, pady=10)
        self.topic_entry.insert(0, "The future of artificial intelligence in education")
        
        # Character Selection
        char_frame = self.create_section_frame(left_frame, "👥 AI Characters", self.colors['bg_light'])
        char_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.char_vars = {}
        for char_name, char_info in self.characters.items():
            char_container = tk.Frame(char_frame, bg=self.colors['bg_light'])
            char_container.pack(fill=tk.X, padx=15, pady=5)
            
            var = tk.BooleanVar(value=True)
            self.char_vars[char_name] = var
            
            cb = tk.Checkbutton(char_container,
                               text=f"{char_name}: {char_info['personality']}",
                               variable=var,
                               bg=self.colors['bg_light'],
                               fg=self.colors['text_light'],
                               selectcolor=self.colors['accent'],
                               activebackground=self.colors['bg_light'],
                               activeforeground=self.colors['text_light'],
                               font=('Helvetica', 10))
            cb.pack(anchor=tk.W)
        
        # Control Buttons
        control_frame = self.create_section_frame(left_frame, "🎮 Controls", self.colors['bg_light'])
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Start/Stop button
        self.start_button = tk.Button(control_frame,
                                     text="🚀 Start Discussion",
                                     command=self.start_discussion,
                                     bg=self.colors['success'],
                                     fg=self.colors['text_light'],
                                     font=('Helvetica', 12, 'bold'),
                                     relief=tk.FLAT,
                                     padx=20,
                                     pady=10)
        self.start_button.pack(fill=tk.X, padx=15, pady=(10, 5))
        
        self.stop_button = tk.Button(control_frame,
                                    text="⏹️ Stop Discussion",
                                    command=self.stop_discussion,
                                    state=tk.DISABLED,
                                    bg=self.colors['error'],
                                    fg=self.colors['text_light'],
                                    font=('Helvetica', 12, 'bold'),
                                    relief=tk.FLAT,
                                    padx=20,
                                    pady=10)
        self.stop_button.pack(fill=tk.X, padx=15, pady=(5, 10))
        
        # User Input Section
        user_frame = self.create_section_frame(left_frame, "💬 Your Response", self.colors['bg_light'])
        user_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Text input
        self.user_text_entry = tk.Entry(user_frame,
                                       font=('Helvetica', 12),
                                       bg=self.colors['bg_dark'],
                                       fg=self.colors['text_light'],
                                       insertbackground=self.colors['accent'])
        self.user_text_entry.pack(fill=tk.X, padx=15, pady=(10, 5))
        
        # Button row
        button_row = tk.Frame(user_frame, bg=self.colors['bg_light'])
        button_row.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.send_text_button = tk.Button(button_row,
                                         text="📤 Send",
                                         command=self.send_text_response,
                                         bg=self.colors['accent'],
                                         fg=self.colors['text_light'],
                                         font=('Helvetica', 10, 'bold'),
                                         relief=tk.FLAT,
                                         padx=15,
                                         pady=5)
        self.send_text_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.speak_text_button = tk.Button(button_row,
                                          text="🔊 Speak",
                                          command=self.speak_text_response,
                                          bg=self.colors['bg_light'],
                                          fg=self.colors['text_light'],
                                          font=('Helvetica', 10, 'bold'),
                                          relief=tk.FLAT,
                                          padx=15,
                                          pady=5)
        self.speak_text_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Voice recording button
        self.record_button = tk.Button(user_frame,
                                      text="🎤 Record Voice",
                                      command=self.toggle_recording,
                                      bg=self.colors['warning'],
                                      fg=self.colors['text_dark'],
                                      font=('Helvetica', 10, 'bold'),
                                      relief=tk.FLAT,
                                      padx=15,
                                      pady=5)
        self.record_button.pack(fill=tk.X, padx=15, pady=(5, 10))
        
        # Save button
        save_button = tk.Button(left_frame,
                               text="💾 Save Discussion",
                               command=self.save_discussion,
                               bg=self.colors['bg_light'],
                               fg=self.colors['text_light'],
                               font=('Helvetica', 12, 'bold'),
                               relief=tk.FLAT,
                               padx=20,
                               pady=10)
        save_button.pack(fill=tk.X, pady=(0, 15))
        
        return left_frame
        
    def create_right_panel(self, parent):
        """Create right discussion panel"""
        right_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        
        # Discussion header
        discussion_header = tk.Label(right_frame,
                                   text="💭 Live Discussion",
                                   font=('Helvetica', 16, 'bold'),
                                   bg=self.colors['bg_medium'],
                                   fg=self.colors['text_light'])
        discussion_header.pack(pady=(20, 10))
        
        # Discussion text area
        text_frame = tk.Frame(right_frame, bg=self.colors['bg_light'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.discussion_text = scrolledtext.ScrolledText(
            text_frame,
            height=20,
            wrap=tk.WORD,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_light'],
            font=('Helvetica', 11),
            insertbackground=self.colors['accent'],
            selectbackground=self.colors['accent'],
            selectforeground=self.colors['text_light']
        )
        self.discussion_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        return right_frame
        
    def create_section_frame(self, parent, title, bg_color):
        """Create a section frame with title"""
        frame = tk.Frame(parent, bg=bg_color, relief=tk.RAISED, borderwidth=2)
        
        title_label = tk.Label(frame,
                              text=title,
                              font=('Helvetica', 12, 'bold'),
                              bg=bg_color,
                              fg=self.colors['text_light'])
        title_label.pack(pady=10)
        
        return frame
        
    def create_status_bar(self, parent):
        """Create modern status bar"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_medium'], height=40)
        status_frame.pack(fill=tk.X, pady=(20, 0))
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_var.set("🚀 Ready to start discussion")
        
        status_label = tk.Label(status_frame,
                               textvariable=self.status_var,
                               font=('Helvetica', 10),
                               bg=self.colors['bg_medium'],
                               fg=self.colors['text_light'])
        status_label.pack(expand=True)
        
        # Bind Enter key to send text
        self.user_text_entry.bind('<Return>', lambda e: self.send_text_response())
        
    def test_api_connection(self):
        """Test the ElevenLabs API connection"""
        try:
            # Test by getting available voices
            available_voices = voices()
            
            # Check if our character voices are available
            available_voice_ids = [voice.voice_id for voice in available_voices]
            missing_voices = []
            
            for char_name, char_info in self.characters.items():
                if char_info['voice_id'] not in available_voice_ids:
                    missing_voices.append(f"{char_name} ({char_info['voice_id']})")
            
            if missing_voices:
                messagebox.showwarning("Warning", 
                                     f"Some character voices are not available:\n{', '.join(missing_voices)}")
            else:
                messagebox.showinfo("Success", "🎉 API connection successful! All character voices available.")
            
            self.status_var.set("✅ API connection successful")
            
        except Exception as e:
            messagebox.showerror("API Error", f"❌ API connection failed:\n{str(e)}")
            self.status_var.set("❌ API connection failed")
    
    def validate_setup(self) -> Tuple[bool, str]:
        """Validate the application setup"""
        if not self.topic:
            return False, "Please enter a discussion topic"
        
        if not self.microphone:
            return False, "Microphone not available"
        
        # Check if at least one character is selected
        active_characters = [name for name, var in self.char_vars.items() if var.get()]
        if not active_characters:
            return False, "Please select at least one character for the discussion"
        
        return True, ""
    
    def start_discussion(self):
        """Start the AI discussion"""
        # Validate setup
        is_valid, error_msg = self.validate_setup()
        if not is_valid:
            messagebox.showerror("Error", error_msg)
            return
        
        self.topic = self.topic_entry.get().strip()
        self.discussion_history = []
        self.current_speaker = None
        self.discussion_active = True
        
        # Get active characters
        self.active_characters = [name for name, var in self.char_vars.items() if var.get()]
        
        # Update UI state
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.topic_entry.config(state=tk.DISABLED)
        
        # Start AI discussion thread
        self.discussion_thread = threading.Thread(target=self.run_ai_discussion, daemon=True)
        self.discussion_thread.start()
        
        self.status_var.set("🎭 Discussion started - AI characters are discussing the topic")
    
    def stop_discussion(self):
        """Stop the AI discussion"""
        self.discussion_active = False
        self.recording = False
        self.playing = False
        
        # Update UI state
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.topic_entry.config(state=tk.NORMAL)
        
        self.status_var.set("⏹️ Discussion stopped")
    
    def run_ai_discussion(self):
        """Run the AI discussion in a separate thread"""
        try:
            # Start with first active character
            self.current_speaker = self.active_characters[0]
            
            # Generate initial response
            initial_response = self.generate_ai_response(
                f"Introduce the topic '{self.topic}' and start the discussion",
                self.current_speaker
            )
            
            if initial_response:
                self.add_to_discussion(self.current_speaker, initial_response)
                self.play_audio_response(initial_response, self.characters[self.current_speaker]['voice_id'])
            
            # Continue discussion with turn-taking
            turn_count = 0
            while self.discussion_active and turn_count < DISCUSSION_CONFIG['max_turns']:
                time.sleep(DISCUSSION_CONFIG['turn_delay'])
                
                if not self.discussion_active:
                    break
                
                # Switch to next speaker
                current_index = self.active_characters.index(self.current_speaker)
                next_index = (current_index + 1) % len(self.active_characters)
                self.current_speaker = self.active_characters[next_index]
                
                # Generate response
                response = self.generate_ai_response(
                    f"Continue the discussion about '{self.topic}' from {self.current_speaker}'s perspective",
                    self.current_speaker
                )
                
                if response:
                    self.add_to_discussion(self.current_speaker, response)
                    self.play_audio_response(response, self.characters[self.current_speaker]['voice_id'])
                    turn_count += 1
                
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ Discussion error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Discussion failed: {str(e)}"))
    
    def generate_ai_response(self, prompt: str, character: str) -> Optional[str]:
        """Generate AI response using ElevenLabs API"""
        try:
            # For now, we'll use a simple approach
            # In a full implementation, you'd use the ElevenLabs agent API
            responses = {
                'Alex': [
                    "I think this is a fantastic opportunity for us to explore new possibilities.",
                    "Let's focus on the positive aspects and how we can make this work together.",
                    "I'm excited about the potential here - we just need to take that first step.",
                    "This could really transform how we approach the entire field.",
                    "I believe we're on the right track with this direction."
                ],
                'Jordan': [
                    "That's an interesting point, but I have some concerns we should address.",
                    "We need to carefully consider the implications before moving forward.",
                    "I'd like to understand the risks involved in this approach.",
                    "Let me play devil's advocate here for a moment.",
                    "We should examine the data more carefully before making decisions."
                ],
                'Taylor': [
                    "What if we approached this from a completely different angle?",
                    "I'm thinking outside the box here - maybe we need a paradigm shift.",
                    "Let's get creative and explore some unconventional solutions.",
                    "This reminds me of a completely different problem we solved last year.",
                    "I have a wild idea that might just work."
                ]
            }
            
            import random
            return random.choice(responses[character])
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ AI response error: {str(e)}"))
            return None
    
    def add_to_discussion(self, speaker: str, message: str):
        """Add a message to the discussion display"""
        timestamp = time.strftime("%H:%M:%S")
        
        # Color code speakers
        if speaker == "You":
            formatted_message = f"[{timestamp}] 👤 {speaker}: {message}\n"
        else:
            formatted_message = f"[{timestamp}] 🤖 {speaker}: {message}\n"
        
        self.root.after(0, lambda: self.discussion_text.insert(tk.END, formatted_message))
        self.root.after(0, lambda: self.discussion_text.see(tk.END))
        
        self.discussion_history.append({
            'speaker': speaker,
            'message': message,
            'timestamp': timestamp
        })
    
    def play_audio_response(self, text: str, voice_id: str):
        """Play audio response using ElevenLabs TTS"""
        try:
            # Generate audio using ElevenLabs
            audio = generate(
                text=text,
                voice=voice_id,
                model="eleven_monolingual_v1"
            )
            
            # Save to temporary file and play
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio)
                temp_filename = temp_file.name
            
            # Play audio in separate thread
            threading.Thread(target=self._play_audio_file, 
                           args=(temp_filename,), daemon=True).start()
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ Audio generation error: {str(e)}"))
    
    def _play_audio_file(self, filename: str):
        """Play audio file and clean up"""
        try:
            # Play audio using sounddevice
            data, samplerate = sd.read(filename)
            sd.play(data, samplerate)
            sd.wait()
            
            # Clean up temporary file
            os.unlink(filename)
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ Audio playback error: {str(e)}"))
    
    def send_text_response(self):
        """Send text response from user"""
        text = self.user_text_entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to send")
            return
        
        # Add user message to discussion
        self.add_to_discussion("You", text)
        
        # Clear the input field
        self.user_text_entry.delete(0, tk.END)
        
        # Generate AI response
        self.generate_user_response(text)
        
        self.status_var.set("📤 Text message sent")
    
    def speak_text_response(self):
        """Convert user's text to speech and play it"""
        text = self.user_text_entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to speak")
            return
        
        # Add user message to discussion
        self.add_to_discussion("You", text)
        
        # Generate and play TTS for user message
        self.play_user_tts(text)
        
        # Clear the input field
        self.user_text_entry.delete(0, tk.END)
        
        # Generate AI response
        self.generate_user_response(text)
        
        self.status_var.set("🔊 Text spoken and sent")
    
    def play_user_tts(self, text: str):
        """Play TTS for user message using a default voice"""
        try:
            # Use the first available character voice for user TTS
            default_voice_id = self.characters['Alex']['voice_id']
            
            # Generate audio using ElevenLabs
            audio = generate(
                text=text,
                voice=default_voice_id,
                model="eleven_monolingual_v1"
            )
            
            # Save to temporary file and play
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio)
                temp_filename = temp_file.name
            
            # Play audio in separate thread
            threading.Thread(target=self._play_audio_file, 
                           args=(temp_filename,), daemon=True).start()
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ User TTS error: {str(e)}"))
    
    def toggle_recording(self):
        """Toggle voice recording for user input"""
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording user voice input"""
        if not self.microphone:
            messagebox.showerror("Error", "Microphone not available")
            return
        
        self.recording = True
        self.record_button.config(text="⏹️ Stop Recording", bg=self.colors['error'])
        self.status_var.set("🎤 Recording... Speak now!")
        
        # Start recording thread
        self.recording_thread = threading.Thread(target=self.record_audio, daemon=True)
        self.recording_thread.start()
    
    def stop_recording(self):
        """Stop recording user voice input"""
        self.recording = False
        self.record_button.config(text="🎤 Record Voice", bg=self.colors['warning'])
        self.status_var.set("⏹️ Recording stopped")
    
    def record_audio(self):
        """Record audio from microphone - IMPROVED VERSION"""
        try:
            # Use a more reliable recording approach
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio with better parameters
                audio = self.recognizer.listen(
                    source,
                    timeout=10,  # Increased timeout
                    phrase_time_limit=15,  # Increased phrase limit
                    snowboy_configuration=None  # Disable snowboy for better compatibility
                )
                
                # Convert speech to text
                try:
                    text = self.recognizer.recognize_google(audio)
                    
                    if text:
                        self.root.after(0, lambda: self.add_to_discussion("You", text))
                        self.root.after(0, lambda: self.status_var.set(f"🎯 Recognized: {text}"))
                        
                        # Generate AI response to user input
                        self.generate_user_response(text)
                    else:
                        self.root.after(0, lambda: self.status_var.set("⚠️ No speech detected"))
                        
                except sr.UnknownValueError:
                    self.root.after(0, lambda: self.status_var.set("❌ Could not understand speech"))
                except sr.RequestError as e:
                    self.root.after(0, lambda: self.status_var.set(f"❌ Speech recognition error: {str(e)}"))
                    
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.status_var.set("⏰ Recording timeout - no speech detected"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ Recording error: {str(e)}"))
        
        finally:
            if self.recording:
                # Continue recording if still active
                time.sleep(0.1)  # Small delay to prevent CPU overload
                self.record_audio()
    
    def generate_user_response(self, user_input: str):
        """Generate AI response to user input"""
        try:
            # Select next speaker
            current_index = self.active_characters.index(self.current_speaker)
            next_index = (current_index + 1) % len(self.active_characters)
            next_speaker = self.active_characters[next_index]
            
            self.current_speaker = next_speaker
            
            # Generate response
            response = self.generate_ai_response(
                f"Respond to the user's input: '{user_input}' from {next_speaker}'s perspective",
                next_speaker
            )
            
            if response:
                self.add_to_discussion(next_speaker, response)
                self.play_audio_response(response, self.characters[next_speaker]['voice_id'])
                
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ Response generation error: {str(e)}"))
    
    def save_discussion(self):
        """Save the discussion to a file"""
        if not self.discussion_history:
            messagebox.showwarning("Warning", "No discussion to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    # Save as JSON
                    with open(filename, 'w') as f:
                        json.dump({
                            'topic': self.topic,
                            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                            'discussion': self.discussion_history
                        }, f, indent=2)
                else:
                    # Save as text
                    with open(filename, 'w') as f:
                        f.write(f"Discussion Topic: {self.topic}\n")
                        f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("=" * 50 + "\n\n")
                        
                        for entry in self.discussion_history:
                            f.write(f"[{entry['timestamp']}] {entry['speaker']}: {entry['message']}\n")
                
                messagebox.showinfo("Success", f"💾 Discussion saved to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"❌ Failed to save discussion: {str(e)}")
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.stop_discussion()
        finally:
            # Cleanup
            if hasattr(self, 'audio') and self.audio:
                self.audio.terminate()

def main():
    """Main entry point"""
    try:
        app = ModernVoiceDiscussionSimulator()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Fatal Error", f"Application failed to start: {str(e)}")

if __name__ == "__main__":
    main()