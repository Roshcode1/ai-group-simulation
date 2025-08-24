#!/usr/bin/env python3
"""
Enhanced Voice-Based Group Discussion Simulator
A real-time AI-powered group discussion simulator using ElevenLabs Conversational AI API
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

# Add config directory to path
sys.path.append(str(Path(__file__).parent.parent / 'config'))
from config import CHARACTERS, AUDIO_CONFIG, DISCUSSION_CONFIG, UI_CONFIG, ERROR_MESSAGES, SUCCESS_MESSAGES

class EnhancedVoiceDiscussionSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Enhanced Voice Discussion Simulator")
        self.root.geometry(UI_CONFIG['window_size'])
        self.root.configure(bg='#2b2b2b')
        
        # ElevenLabs API configuration
        self.api_key = None
        self.agent_id = None
        self.voices_available = []
        
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
        self.user_input_queue = queue.Queue()
        self.ai_response_queue = queue.Queue()
        self.discussion_active = False
        
        # Audio components
        self.audio = None
        self.recognizer = sr.Recognizer()
        self.microphone = None
        
        # Initialize components
        self.initialize_audio()
        self.setup_ui()
        
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
    
    def setup_ui(self):
        """Initialize the user interface"""
        # Configure style
        style = ttk.Style()
        style.theme_use(UI_CONFIG['theme'])
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Enhanced Voice Discussion Simulator", 
                               font=(UI_CONFIG['font_family'], UI_CONFIG['title_font_size'], 'bold'))
        title_label.pack(pady=(0, 20))
        
        # API Key input section
        api_frame = ttk.LabelFrame(main_frame, text="ElevenLabs API Configuration", padding=10)
        api_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(api_frame, text="API Key:").pack(anchor=tk.W)
        self.api_key_entry = ttk.Entry(api_frame, width=60, show="*")
        self.api_key_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Load API key from environment if available
        env_api_key = os.getenv('ELEVENLABS_API_KEY')
        if env_api_key:
            self.api_key_entry.insert(0, env_api_key)
        
        ttk.Label(api_frame, text="Agent ID (optional):").pack(anchor=tk.W)
        self.agent_id_entry = ttk.Entry(api_frame, width=60)
        self.agent_id_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Test API button
        test_api_button = ttk.Button(api_frame, text="Test API Connection", 
                                    command=self.test_api_connection)
        test_api_button.pack(pady=(0, 5))
        
        # Topic input section
        topic_frame = ttk.LabelFrame(main_frame, text="Discussion Topic", padding=10)
        topic_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(topic_frame, text="Enter the discussion topic:").pack(anchor=tk.W)
        self.topic_entry = ttk.Entry(topic_frame, width=60)
        self.topic_entry.pack(fill=tk.X, pady=(0, 5))
        self.topic_entry.insert(0, "The future of artificial intelligence in education")
        
        # Character selection
        char_frame = ttk.LabelFrame(main_frame, text="Character Configuration", padding=10)
        char_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.char_vars = {}
        for char_name, char_info in self.characters.items():
            var = tk.BooleanVar(value=True)
            self.char_vars[char_name] = var
            cb = ttk.Checkbutton(char_frame, text=f"{char_name}: {char_info['personality']}", 
                                variable=var)
            cb.pack(anchor=tk.W)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="Start Discussion", 
                                      command=self.start_discussion)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="Stop Discussion", 
                                     command=self.stop_discussion, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.record_button = ttk.Button(control_frame, text="🎤 Record", 
                                       command=self.toggle_recording)
        self.record_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_button = ttk.Button(control_frame, text="💾 Save Discussion", 
                                     command=self.save_discussion)
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # User input section
        user_input_frame = ttk.LabelFrame(main_frame, text="Your Response", padding=10)
        user_input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Text input for user
        ttk.Label(user_input_frame, text="Type your response:").pack(anchor=tk.W)
        self.user_text_entry = ttk.Entry(user_input_frame, width=50)
        self.user_text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Send text button
        self.send_text_button = ttk.Button(user_input_frame, text="Send Text", 
                                          command=self.send_text_response)
        self.send_text_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Speak text button (TTS)
        self.speak_text_button = ttk.Button(user_input_frame, text="🔊 Speak Text", 
                                           command=self.speak_text_response)
        self.speak_text_button.pack(side=tk.LEFT)
        
        # Discussion display
        discussion_frame = ttk.LabelFrame(main_frame, text="Discussion", padding=10)
        discussion_frame.pack(fill=tk.BOTH, expand=True)
        
        self.discussion_text = scrolledtext.ScrolledText(discussion_frame, height=15, 
                                                        wrap=tk.WORD, bg='#f0f0f0',
                                                        font=(UI_CONFIG['font_family'], UI_CONFIG['font_size']))
        self.discussion_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to start discussion")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Bind Enter key to send text
        self.user_text_entry.bind('<Return>', lambda e: self.send_text_response())
        
    def test_api_connection(self):
        """Test the ElevenLabs API connection"""
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Error", ERROR_MESSAGES['api_key_missing'])
            return
        
        try:
            set_api_key(api_key)
            
            # Test by getting available voices
            available_voices = voices()
            self.voices_available = available_voices
            
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
                messagebox.showinfo("Success", "API connection successful! All character voices available.")
            
            self.api_key = api_key
            self.status_var.set(SUCCESS_MESSAGES['api_key_valid'])
            
        except Exception as e:
            messagebox.showerror("API Error", f"{ERROR_MESSAGES['api_key_invalid']}\nDetails: {str(e)}")
    
    def validate_setup(self) -> Tuple[bool, str]:
        """Validate the application setup"""
        if not self.api_key:
            return False, ERROR_MESSAGES['api_key_missing']
        
        if not self.topic:
            return False, ERROR_MESSAGES['topic_missing']
        
        if not self.microphone:
            return False, ERROR_MESSAGES['audio_init_failed']
        
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
        self.api_key_entry.config(state=tk.DISABLED)
        self.agent_id_entry.config(state=tk.DISABLED)
        
        # Start AI discussion thread
        self.discussion_thread = threading.Thread(target=self.run_ai_discussion, daemon=True)
        self.discussion_thread.start()
        
        self.status_var.set("Discussion started - AI characters are discussing the topic")
    
    def stop_discussion(self):
        """Stop the AI discussion"""
        self.discussion_active = False
        self.recording = False
        self.playing = False
        
        # Update UI state
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.topic_entry.config(state=tk.NORMAL)
        self.api_key_entry.config(state=tk.NORMAL)
        self.agent_id_entry.config(state=tk.NORMAL)
        
        self.status_var.set("Discussion stopped")
    
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
            self.root.after(0, lambda: self.status_var.set(f"Discussion error: {str(e)}"))
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
            self.root.after(0, lambda: self.status_var.set(f"AI response error: {str(e)}"))
            return None
    
    def add_to_discussion(self, speaker: str, message: str):
        """Add a message to the discussion display"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {speaker}: {message}\n"
        
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
            self.root.after(0, lambda: self.status_var.set(f"Audio generation error: {str(e)}"))
    
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
            self.root.after(0, lambda: self.status_var.set(f"Audio playback error: {str(e)}"))
    
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
        
        self.status_var.set("Text message sent")
    
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
        
        self.status_var.set("Text spoken and sent")
    
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
            self.root.after(0, lambda: self.status_var.set(f"User TTS error: {str(e)}"))
    
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
        self.record_button.config(text="⏹️ Stop Recording")
        self.status_var.set("Recording... Speak now!")
        
        # Start recording thread
        self.recording_thread = threading.Thread(target=self.record_audio, daemon=True)
        self.recording_thread.start()
    
    def stop_recording(self):
        """Stop recording user voice input"""
        self.recording = False
        self.record_button.config(text="🎤 Record")
        self.status_var.set("Recording stopped")
    
    def record_audio(self):
        """Record audio from microphone"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, 
                                            timeout=AUDIO_CONFIG['timeout'], 
                                            phrase_time_limit=AUDIO_CONFIG['phrase_time_limit'])
                
                # Convert speech to text
                text = self.recognizer.recognize_google(audio)
                
                if text:
                    self.root.after(0, lambda: self.add_to_discussion("You", text))
                    self.root.after(0, lambda: self.status_var.set(f"Recognized: {text}"))
                    
                    # Generate AI response to user input
                    self.generate_user_response(text)
                    
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.status_var.set("No speech detected"))
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.status_var.set("Could not understand speech"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Recording error: {str(e)}"))
        
        finally:
            if self.recording:
                # Continue recording if still active
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
            self.root.after(0, lambda: self.status_var.set(f"Response generation error: {str(e)}"))
    
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
                
                messagebox.showinfo("Success", f"Discussion saved to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save discussion: {str(e)}")
    
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
        app = EnhancedVoiceDiscussionSimulator()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Fatal Error", f"Application failed to start: {str(e)}")

if __name__ == "__main__":
    main()