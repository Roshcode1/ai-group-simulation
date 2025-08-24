#!/usr/bin/env python3
"""
Test script to verify Voice Discussion Simulator installation
"""

import sys
import importlib
from pathlib import Path

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        if package_name:
            importlib.import_module(package_name)
        else:
            importlib.import_module(module_name)
        print(f"✅ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - FAILED: {e}")
        return False

def test_audio_devices():
    """Test audio device availability"""
    print("\n🔊 Testing audio devices...")
    
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        
        # Check input devices
        input_devices = []
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append(device_info['name'])
        
        if input_devices:
            print(f"✅ Found {len(input_devices)} input device(s):")
            for device in input_devices[:3]:  # Show first 3
                print(f"   - {device}")
        else:
            print("⚠️  No input devices found")
        
        # Check output devices
        output_devices = []
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxOutputChannels'] > 0:
                output_devices.append(device_info['name'])
        
        if output_devices:
            print(f"✅ Found {len(output_devices)} output device(s):")
            for device in output_devices[:3]:  # Show first 3
                print(f"   - {device}")
        else:
            print("⚠️  No output devices found")
        
        audio.terminate()
        return True
        
    except Exception as e:
        print(f"❌ Audio device test failed: {e}")
        return False

def test_elevenlabs_connection():
    """Test ElevenLabs API connection (without API key)"""
    print("\n🌐 Testing ElevenLabs API...")
    
    try:
        from elevenlabs import voices
        print("✅ ElevenLabs library imported successfully")
        print("ℹ️  Note: API connection test requires valid API key")
        return True
    except ImportError as e:
        print(f"❌ ElevenLabs library not available: {e}")
        return False

def test_speech_recognition():
    """Test speech recognition setup"""
    print("\n🎤 Testing speech recognition...")
    
    try:
        import speech_recognition as sr
        
        # Test microphone initialization
        try:
            mic = sr.Microphone()
            print("✅ Microphone initialized")
            
            # Test recognizer
            recognizer = sr.Recognizer()
            print("✅ Speech recognizer initialized")
            
            return True
            
        except Exception as e:
            print(f"⚠️  Microphone test failed: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Speech recognition not available: {e}")
        return False

def test_config_files():
    """Test if configuration files exist"""
    print("\n📁 Testing configuration files...")
    
    config_dir = Path(__file__).parent / "config"
    config_file = config_dir / "config.py"
    
    if config_file.exists():
        print("✅ Configuration file found")
        
        # Try to import config
        try:
            sys.path.append(str(config_dir))
            import config
            print("✅ Configuration imported successfully")
            return True
        except Exception as e:
            print(f"⚠️  Configuration import failed: {e}")
            return False
    else:
        print("❌ Configuration file not found")
        return False

def main():
    """Main test function"""
    print("🧪 Voice Discussion Simulator - Installation Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test core dependencies
    print("\n📦 Testing core dependencies...")
    
    dependencies = [
        ("tkinter", None),
        ("threading", None),
        ("queue", None),
        ("tempfile", None),
        ("json", None),
        ("numpy", "numpy"),
        ("sounddevice", "sounddevice"),
        ("pyaudio", "pyaudio"),
        ("speech_recognition", "speechrecognition"),
        ("elevenlabs", "elevenlabs"),
    ]
    
    for module_name, package_name in dependencies:
        total_tests += 1
        if test_import(module_name, package_name):
            tests_passed += 1
    
    # Test configuration
    total_tests += 1
    if test_config_files():
        tests_passed += 1
    
    # Test audio devices
    total_tests += 1
    if test_audio_devices():
        tests_passed += 1
    
    # Test ElevenLabs
    total_tests += 1
    if test_elevenlabs_connection():
        tests_passed += 1
    
    # Test speech recognition
    total_tests += 1
    if test_speech_recognition():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Installation is complete.")
        print("\n🚀 You can now run the simulator with:")
        print("   python run.py")
        print("   or")
        print("   python src/enhanced_simulator.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n📋 Common solutions:")
        print("1. Run: python setup.py")
        print("2. Install missing system dependencies")
        print("3. Check your Python environment")
    
    print("\n💡 For help, see README.md or run: python setup.py")

if __name__ == "__main__":
    main()