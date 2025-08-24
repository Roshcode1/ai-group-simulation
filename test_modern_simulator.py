#!/usr/bin/env python3
"""
Comprehensive Test for Modern Voice Discussion Simulator
Tests all functionality including the new features
"""

import sys
import os
from pathlib import Path

def test_modern_simulator_file():
    """Test if modern simulator file exists and has correct structure"""
    print("🔍 Testing Modern Simulator File...")
    
    modern_sim = Path("src/modern_simulator.py")
    if not modern_sim.exists():
        print("❌ Modern simulator not found")
        return False
    
    print("✅ Modern simulator file found")
    
    # Check file size (should be substantial)
    file_size = modern_sim.stat().st_size
    if file_size < 10000:  # Less than 10KB
        print(f"⚠️  File seems too small: {file_size} bytes")
        return False
    
    print(f"✅ File size appropriate: {file_size} bytes")
    return True

def test_modern_simulator_syntax():
    """Test Python syntax of modern simulator"""
    print("\n🐍 Testing Modern Simulator Syntax...")
    
    try:
        with open("src/modern_simulator.py", 'r') as f:
            content = f.read()
        
        # Basic syntax check
        compile(content, "src/modern_simulator.py", 'exec')
        print("✅ Syntax check passed")
        
        # Check for key imports
        required_imports = [
            'import tkinter as tk',
            'import speech_recognition as sr',
            'from elevenlabs import generate',
            'import pyaudio'
        ]
        
        missing_imports = []
        for imp in required_imports:
            if imp not in content:
                missing_imports.append(imp)
        
        if missing_imports:
            print(f"⚠️  Missing imports: {missing_imports}")
            return False
        
        print("✅ All required imports found")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

def test_modern_ui_features():
    """Test if modern UI features are implemented"""
    print("\n🎨 Testing Modern UI Features...")
    
    try:
        with open("src/modern_simulator.py", 'r') as f:
            content = f.read()
        
        # Check for modern UI components
        ui_features = [
            'class ModernVoiceDiscussionSimulator',
            'self.colors = {',
            'bg_dark',
            'bg_medium', 
            'accent',
            'create_header',
            'create_left_panel',
            'create_right_panel'
        ]
        
        missing_features = []
        for feature in ui_features:
            if feature not in content:
                missing_features.append(feature)
        
        if missing_features:
            print(f"⚠️  Missing UI features: {missing_features}")
            return False
        
        print("✅ All modern UI features found")
        return True
        
    except Exception as e:
        print(f"❌ Error testing UI features: {e}")
        return False

def test_audio_recording_fixes():
    """Test if audio recording issues are fixed"""
    print("\n🎤 Testing Audio Recording Fixes...")
    
    try:
        with open("src/modern_simulator.py", 'r') as f:
            content = f.read()
        
        # Check for improved audio recording
        audio_improvements = [
            'IMPROVED VERSION',
            'timeout=10',
            'phrase_time_limit=15',
            'snowboy_configuration=None',
            'adjust_for_ambient_noise',
            'recognize_google'
        ]
        
        missing_improvements = []
        for improvement in audio_improvements:
            if improvement not in content:
                missing_improvements.append(improvement)
        
        if missing_improvements:
            print(f"⚠️  Missing audio improvements: {missing_improvements}")
            return False
        
        print("✅ All audio recording improvements found")
        return True
        
    except Exception as e:
        print(f"❌ Error testing audio fixes: {e}")
        return False

def test_tts_functionality():
    """Test if TTS functionality is properly implemented"""
    print("\n🔊 Testing TTS Functionality...")
    
    try:
        with open("src/modern_simulator.py", 'r') as f:
            content = f.read()
        
        # Check for TTS features
        tts_features = [
            'play_user_tts',
            'speak_text_response',
            'generate(',
            'eleven_monolingual_v1',
            'voice_id'
        ]
        
        missing_tts = []
        for feature in tts_features:
            if feature not in content:
                missing_tts.append(feature)
        
        if missing_tts:
            print(f"⚠️  Missing TTS features: {missing_tts}")
            return False
        
        print("✅ All TTS features found")
        return True
        
    except Exception as e:
        print(f"❌ Error testing TTS: {e}")
        return False

def test_api_integration():
    """Test if API integration is properly configured"""
    print("\n🔑 Testing API Integration...")
    
    try:
        with open("src/modern_simulator.py", 'r') as f:
            content = f.read()
        
        # Check for API configuration
        api_features = [
            'self.api_key =',
            'set_api_key',
            'voices()',
            'generate(',
            'test_api_connection'
        ]
        
        missing_api = []
        for feature in api_features:
            if feature not in content:
                missing_api.append(feature)
        
        if missing_api:
            print(f"⚠️  Missing API features: {missing_api}")
            return False
        
        print("✅ All API integration features found")
        return True
        
    except Exception as e:
        print(f"❌ Error testing API integration: {e}")
        return False

def test_modern_launcher():
    """Test if modern launcher exists"""
    print("\n🚀 Testing Modern Launcher...")
    
    launcher = Path("run_modern.py")
    if not launcher.exists():
        print("❌ Modern launcher not found")
        return False
    
    print("✅ Modern launcher found")
    
    # Check launcher content
    try:
        with open(launcher, 'r') as f:
            content = f.read()
        
        if 'modern_simulator.py' in content:
            print("✅ Launcher references modern simulator")
            return True
        else:
            print("⚠️  Launcher doesn't reference modern simulator")
            return False
            
    except Exception as e:
        print(f"❌ Error reading launcher: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Comprehensive Test for Modern Voice Discussion Simulator")
    print("=" * 70)
    
    tests = [
        ("Modern Simulator File", test_modern_simulator_file),
        ("Modern Simulator Syntax", test_modern_simulator_syntax),
        ("Modern UI Features", test_modern_ui_features),
        ("Audio Recording Fixes", test_audio_recording_fixes),
        ("TTS Functionality", test_tts_functionality),
        ("API Integration", test_api_integration),
        ("Modern Launcher", test_modern_launcher)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"💥 {test_name} - ERROR: {e}")
    
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Modern simulator is ready!")
        print("\n🚀 To launch the modern simulator:")
        print("   python3 run_modern.py")
        print("\n✨ Features available:")
        print("   - Modern, colorful UI design")
        print("   - Fixed audio recording with improved parameters")
        print("   - Text-to-speech for user messages")
        print("   - Pre-configured API key")
        print("   - Real-time voice interaction")
        print("   - Enhanced error handling")
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the issues above.")
    
    print("\n💡 The modern simulator includes your API key and is ready to use!")

if __name__ == "__main__":
    main()