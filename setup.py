#!/usr/bin/env python3
"""
Setup script for Voice Discussion Simulator
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8 or higher is required. Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command("python -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    requirements_file = Path(__file__).parent / "requirements.txt"
    if requirements_file.exists():
        if not run_command(f"pip install -r {requirements_file}", "Installing requirements"):
            return False
    else:
        print("⚠️  requirements.txt not found, installing core dependencies...")
        core_deps = [
            "elevenlabs>=0.2.26",
            "PyAudio>=0.2.11",
            "speechrecognition>=3.10.0",
            "sounddevice>=0.4.6",
            "numpy>=1.24.3",
            "python-dotenv>=1.0.0"
        ]
        
        for dep in core_deps:
            if not run_command(f"pip install {dep}", f"Installing {dep}"):
                print(f"⚠️  Failed to install {dep}, continuing...")
    
    return True

def check_system_dependencies():
    """Check and suggest system dependencies"""
    print("🔧 Checking system dependencies...")
    
    # Check for PyAudio
    try:
        import pyaudio
        print("✅ PyAudio is available")
    except ImportError:
        print("❌ PyAudio not found")
        print("\n📋 To install PyAudio, you may need system dependencies:")
        print("\nUbuntu/Debian:")
        print("  sudo apt-get install python3-dev portaudio19-dev python3-pyaudio libasound2-dev")
        print("\nmacOS:")
        print("  brew install portaudio")
        print("\nWindows:")
        print("  pip install pipwin")
        print("  pipwin install pyaudio")
        return False
    
    # Check for other audio libraries
    try:
        import sounddevice
        print("✅ SoundDevice is available")
    except ImportError:
        print("⚠️  SoundDevice not found - some features may not work")
    
    try:
        import speech_recognition
        print("✅ SpeechRecognition is available")
    except ImportError:
        print("⚠️  SpeechRecognition not found - voice input will not work")
    
    return True

def create_env_file():
    """Create .env file template"""
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        print("📝 Creating .env file template...")
        env_content = """# ElevenLabs API Configuration
# Get your API key from: https://elevenlabs.io
ELEVENLABS_API_KEY=your_api_key_here

# Optional: Set default discussion topic
DEFAULT_TOPIC=The future of artificial intelligence in education

# Optional: Set default character voices
# ALEX_VOICE_ID=EXAVITQu4vr4xnSDxMaL
# JORDAN_VOICE_ID=MF3mGyEYCl7XYWbV9V6O
# TAYLOR_VOICE_ID=21m00Tcm4TlvDq8ikWAM
"""
        try:
            with open(env_file, 'w') as f:
                f.write(env_content)
            print("✅ .env file created")
        except Exception as e:
            print(f"⚠️  Could not create .env file: {e}")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("🎤 Voice Discussion Simulator Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Check system dependencies
    if not check_system_dependencies():
        print("⚠️  Some system dependencies may be missing")
        print("Please install them manually and run setup again")
    
    # Create environment file
    create_env_file()
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Get your ElevenLabs API key from https://elevenlabs.io")
    print("2. Add your API key to the .env file or enter it in the app")
    print("3. Run the simulator with: python run.py")
    print("\n🚀 Happy discussing!")

if __name__ == "__main__":
    main()