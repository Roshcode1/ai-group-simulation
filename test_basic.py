#!/usr/bin/env python3
"""
Basic test script for Voice Discussion Simulator
Tests core functionality without requiring full dependencies
"""

import sys
import os
from pathlib import Path

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    if sys.version_info >= (3, 8):
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} - Compatible")
        return True
    else:
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} - Requires 3.8+")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "src/enhanced_simulator.py",
        "src/main.py", 
        "config/config.py",
        "requirements.txt",
        "README.md",
        "setup.py",
        "run.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {len(missing_files)}")
        return False
    else:
        print(f"\n✅ All {len(required_files)} required files present")
        return True

def test_config_import():
    """Test if configuration can be imported"""
    print("\n⚙️  Testing configuration import...")
    
    try:
        # Add config to path
        config_dir = Path("config")
        if config_dir.exists():
            sys.path.insert(0, str(config_dir))
            
            # Try to import config
            import config
            print("✅ Configuration imported successfully")
            
            # Check if key constants exist
            if hasattr(config, 'CHARACTERS'):
                print(f"✅ Found {len(config.CHARACTERS)} character definitions")
            else:
                print("⚠️  CHARACTERS not found in config")
                
            if hasattr(config, 'AUDIO_CONFIG'):
                print("✅ Audio configuration found")
            else:
                print("⚠️  AUDIO_CONFIG not found in config")
                
            return True
            
        else:
            print("❌ Config directory not found")
            return False
            
    except Exception as e:
        print(f"❌ Configuration import failed: {e}")
        return False

def test_basic_syntax():
    """Test basic Python syntax of main files"""
    print("\n🔍 Testing Python syntax...")
    
    python_files = [
        "src/enhanced_simulator.py",
        "src/main.py",
        "config/config.py"
    ]
    
    syntax_errors = []
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Basic syntax check (compile)
            compile(content, file_path, 'exec')
            print(f"✅ {file_path} - Syntax OK")
            
        except SyntaxError as e:
            print(f"❌ {file_path} - Syntax error: {e}")
            syntax_errors.append(file_path)
        except Exception as e:
            print(f"⚠️  {file_path} - Read error: {e}")
    
    if syntax_errors:
        print(f"\n❌ Syntax errors found in {len(syntax_errors)} files")
        return False
    else:
        print("\n✅ All Python files have valid syntax")
        return True

def test_requirements():
    """Test requirements.txt format"""
    print("\n📦 Testing requirements.txt...")
    
    try:
        with open("requirements.txt", 'r') as f:
            content = f.read()
        
        lines = content.strip().split('\n')
        valid_lines = [line for line in lines if line.strip() and not line.startswith('#')]
        
        print(f"✅ Found {len(valid_lines)} dependency lines")
        
        # Check for key dependencies
        key_deps = ['elevenlabs', 'PyAudio', 'speechrecognition']
        found_deps = []
        
        for dep in key_deps:
            if any(dep.lower() in line.lower() for line in valid_lines):
                found_deps.append(dep)
                print(f"✅ {dep} found")
            else:
                print(f"⚠️  {dep} not found")
        
        if len(found_deps) >= 2:
            print(f"✅ Found {len(found_deps)}/{len(key_deps)} key dependencies")
            return True
        else:
            print(f"⚠️  Only {len(found_deps)}/{len(key_deps)} key dependencies found")
            return False
            
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def test_ui_components():
    """Test if UI components are properly defined"""
    print("\n🎨 Testing UI components...")
    
    try:
        with open("src/enhanced_simulator.py", 'r') as f:
            content = f.read()
        
        # Check for key UI components
        ui_components = [
            'class EnhancedVoiceDiscussionSimulator',
            'def setup_ui',
            'def __init__',
            'self.root = tk.Tk()',
            'ttk.Frame',
            'ttk.Button',
            'ttk.Entry'
        ]
        
        found_components = []
        for component in ui_components:
            if component in content:
                found_components.append(component)
        
        print(f"✅ Found {len(found_components)}/{len(ui_components)} UI components")
        
        # Check for new TTS features
        tts_features = [
            'send_text_response',
            'speak_text_response', 
            'play_user_tts',
            'user_text_entry',
            'send_text_button',
            'speak_text_button'
        ]
        
        found_tts = []
        for feature in tts_features:
            if feature in content:
                found_tts.append(feature)
        
        print(f"✅ Found {len(found_tts)}/{len(tts_features)} TTS features")
        
        return len(found_components) >= 5 and len(found_tts) >= 4
        
    except Exception as e:
        print(f"❌ Error testing UI components: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Basic Test for Voice Discussion Simulator")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("File Structure", test_file_structure),
        ("Configuration", test_config_import),
        ("Python Syntax", test_basic_syntax),
        ("Requirements", test_requirements),
        ("UI Components", test_ui_components)
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
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed!")
        print("\n🚀 The application structure is ready for testing.")
        print("Next steps:")
        print("1. Install dependencies: python3 setup.py")
        print("2. Test installation: python3 test_installation.py")
        print("3. Launch application: python3 run.py")
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the issues above.")
    
    print("\n💡 For detailed testing, run: python3 test_installation.py")

if __name__ == "__main__":
    main()