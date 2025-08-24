#!/usr/bin/env python3
"""
Launcher for Modern Voice Discussion Simulator
"""

import sys
import os
from pathlib import Path

def main():
    """Main launcher function"""
    print("🎤 Modern Voice Discussion Simulator")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    # Check if modern simulator exists
    modern_sim = Path("src/modern_simulator.py")
    if not modern_sim.exists():
        print("❌ Error: Modern simulator not found")
        print("Please ensure src/modern_simulator.py exists")
        sys.exit(1)
    
    print("🚀 Launching Modern Voice Discussion Simulator...")
    print("✨ Features:")
    print("   - Modern, colorful UI design")
    print("   - Fixed audio recording")
    print("   - Text-to-speech for user messages")
    print("   - Pre-configured API key")
    print("   - Real-time voice interaction")
    
    # Launch the modern simulator
    os.system(f"python3 {modern_sim}")

if __name__ == "__main__":
    main()