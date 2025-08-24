#!/usr/bin/env python3
"""
Launcher script for the Voice Discussion Simulator
"""

import sys
import os
from pathlib import Path

def main():
    """Main launcher function"""
    print("🎤 Voice Discussion Simulator")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    # Check if required files exist
    src_dir = Path(__file__).parent / "src"
    if not src_dir.exists():
        print("❌ Error: Source directory not found")
        sys.exit(1)
    
    # Check for enhanced simulator
    enhanced_sim = src_dir / "enhanced_simulator.py"
    basic_sim = src_dir / "main.py"
    
    if enhanced_sim.exists():
        print("🚀 Launching Enhanced Simulator...")
        os.system(f"python {enhanced_sim}")
    elif basic_sim.exists():
        print("🚀 Launching Basic Simulator...")
        os.system(f"python {basic_sim}")
    else:
        print("❌ Error: No simulator found")
        sys.exit(1)

if __name__ == "__main__":
    main()