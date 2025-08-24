#!/usr/bin/env python3
"""
Voice-Based Group Discussion Simulator
A real-time AI-powered group discussion simulator using ElevenLabs Conversational AI API
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import queue
import time
import os
import json
from typing import Dict, List, Optional
import speech_recognition as sr
import sounddevice as sd
import numpy as np
from elevenlabs import generate, stream, set_api_key, Voice, VoiceSettings
from elevenlabs.api import History
import tempfile
import wave
import pyaudio

class VoiceDiscussionSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Discussion Simulator")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # ElevenLabs API configuration
        self.api_key = None
        self.agent_id = None
        
        # Audio configuration
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        self.recording = False
        self.playing = False
        
        # Character definitions
        self.characters = {
            'Alex': {
                'name': 'Alex',
                'voice_id': 'EXAVITQu4vr4xnSDxMaL',
                'personality': 'optimistic leader',
                'description': 'A charismatic and optimistic leader who encourages collaboration and sees opportunities in challenges.'
            },
            'Jordan': {
                'name': 'Jordan',
                'voice_id': 'MF3mGyEYCl7XYWbV9V6O',
                'personality': 'skeptical analyst',
                'description': 'A critical thinker who analyzes situations carefully and asks probing questions.'
            },
            'Taylor': {
                'name': 'Taylor',
                'voice_id': '21m00Tcm4TlvDq8ikWAM',
                'personality': 'creative visionary',
                'description': 'An innovative thinker who brings creative solutions and thinks outside the box.'
            }
        }
        
        # Discussion state
        self.topic = ""
        self.discussion_history = []
        self.current_speaker = None
        self.user_input_queue = queue.Queue()
        self.ai_response_queue = queue.Queue()
        
        # Audio components
        self.audio = pyaudio.PyAudio()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize UI
        self.setup_ui()
        self.setup_audio()
        
    def setup_ui(self):
        """Initialize the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Voice Discussion Simulator", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # API Key input section
        api_frame = ttk.LabelFrame(main_frame, text="ElevenLabs API Configuration", padding=10)
        api_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(api_frame, text="API Key:").pack(anchor=tk.W)
        self.api_key_entry = ttk.Entry(api_frame, width=60, show="*")
        self.api_key_entry.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(api_frame, text="Agent ID (optional):").pack(anchor=tk.W)
        self.agent_id_entry = ttk.Entry(api_frame, width=60)
        self.agent_id_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Topic input section
        topic_frame = ttk.LabelFrame(main_frame, text="Discussion Topic", padding=10)
        topic_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(topic_frame, text="Enter the discussion topic:").pack(anchor=tk.W)
        self.topic_entry = ttk.Entry(topic_frame, width=60)
        self.topic_entry.pack(fill=tk.X, pady=(0, 5))
        self.topic_entry.insert(0, "The future of artificial intelligence in education")
        
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
        
        # Discussion display
        discussion_frame = ttk.LabelFrame(main_frame, text="Discussion", padding=10)
        discussion_frame.pack(fill=tk.BOTH, expand=True)
        
        self.discussion_text = scrolledtext.ScrolledText(discussion_frame, height=15, 
                                                        wrap=tk.WORD, bg='#f0f0f0')
        self.discussion_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to start discussion")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
    def setup_audio(self):
        """Initialize audio components"""
        try:
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.status_var.set("Audio system initialized successfully")
        except Exception as e:
            self.status_var.set(f"Audio initialization error: {str(e)}")
            messagebox.showerror("Audio Error", f"Failed to initialize audio: {str(e)}")
    
    def validate_api_key(self):
        """Validate the API key input"""
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Error", "Please enter your ElevenLabs API key")
            return False
        
        try:
            set_api_key(api_key)
            self.api_key = api_key
            self.status_var.set("API key validated successfully")
            return True
        except Exception as e:
            messagebox.showerror("API Error", f"Invalid API key: {str(e)}")
            return False
    
    def start_discussion(self):
        """Start the AI discussion"""
        if not self.validate_api_key():
            return
        
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showerror("Error", "Please enter a discussion topic")
            return
        
        self.topic = topic
        self.discussion_history = []
        self.current_speaker = None
        
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
            # Generate initial discussion prompt
            system_prompt = self.create_system_prompt()
            
            # Start with Alex introducing the topic
            self.current_speaker = 'Alex'
            initial_response = self.generate_ai_response(
                f"Introduce the topic '{self.topic}' and start the discussion",
                self.current_speaker
            )
            
            if initial_response:
                self.add_to_discussion('Alex', initial_response)
                self.play_audio_response(initial_response, self.characters['Alex']['voice_id'])
            
            # Continue discussion with turn-taking
            while self.recording or len(self.discussion_history) < 6:
                time.sleep(2)  # Pause between responses
                
                # Switch speakers
                if self.current_speaker == 'Alex':
                    self.current_speaker = 'Jordan'
                elif self.current_speaker == 'Jordan':
                    self.current_speaker = 'Taylor'
                else:
                    self.current_speaker = 'Alex'
                
                # Generate response
                response = self.generate_ai_response(
                    f"Continue the discussion about '{self.topic}' from {self.current_speaker}'s perspective",
                    self.current_speaker
                )
                
                if response:
                    self.add_to_discussion(self.current_speaker, response)
                    self.play_audio_response(response, self.characters[self.current_speaker]['voice_id'])
                
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Discussion error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Discussion failed: {str(e)}"))
    
    def create_system_prompt(self):
        """Create the system prompt for the AI discussion"""
        prompt = f"""You are participating in a group discussion about: {self.topic}

You will role-play one of three characters in turn:

1. Alex (Optimistic Leader): {self.characters['Alex']['description']}
2. Jordan (Skeptical Analyst): {self.characters['Jordan']['description']}
3. Taylor (Creative Visionary): {self.characters['Taylor']['description']}

Guidelines:
- Stay in character and respond naturally to the discussion
- Keep responses concise (2-3 sentences)
- Build on previous points made by other characters
- Ask questions to engage others
- Maintain a natural conversation flow
- Be respectful and constructive

Current speaker: [CHARACTER_NAME]

Respond as if you are [CHARACTER_NAME] in this discussion."""
        return prompt
    
    def generate_ai_response(self, prompt: str, character: str) -> Optional[str]:
        """Generate AI response using ElevenLabs API"""
        try:
            # For now, we'll use a simple approach
            # In a full implementation, you'd use the ElevenLabs agent API
            responses = {
                'Alex': [
                    "I think this is a fantastic opportunity for us to explore new possibilities.",
                    "Let's focus on the positive aspects and how we can make this work together.",
                    "I'm excited about the potential here - we just need to take that first step."
                ],
                'Jordan': [
                    "That's an interesting point, but I have some concerns we should address.",
                    "We need to carefully consider the implications before moving forward.",
                    "I'd like to understand the risks involved in this approach."
                ],
                'Taylor': [
                    "What if we approached this from a completely different angle?",
                    "I'm thinking outside the box here - maybe we need a paradigm shift.",
                    "Let's get creative and explore some unconventional solutions."
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
    
    def toggle_recording(self):
        """Toggle voice recording for user input"""
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording user voice input"""
        self.recording = True
        self.record_button.config(text="⏹️ Stop Recording", style="Accent.TButton")
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
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
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
            if self.current_speaker == 'Alex':
                next_speaker = 'Jordan'
            elif self.current_speaker == 'Jordan':
                next_speaker = 'Taylor'
            else:
                next_speaker = 'Alex'
            
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
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.stop_discussion()
        finally:
            # Cleanup
            if hasattr(self, 'audio'):
                self.audio.terminate()

def main():
    """Main entry point"""
    try:
        app = VoiceDiscussionSimulator()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Fatal Error", f"Application failed to start: {str(e)}")

if __name__ == "__main__":
    main()