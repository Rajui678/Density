#!/usr/bin/env python3
'''
Installation script for Density-Temperature Lookup Application
'''

import subprocess
import sys
import os

def install_requirements():
    # Install required packages
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False

def main():
    print("Density-Temperature Lookup App - Installation")
    print("=" * 50)
    
    if install_requirements():
        print("\nInstallation completed successfully!")
        print("\nAvailable applications:")
        print("   1. Web App (Basic): python -m streamlit run web_app.py")
        print("   2. Secure Web App: python run_secure_app.py")
        print("   3. Desktop App: python density_temperature_app.py")
        print("\nSee README.md for detailed instructions")
    else:
        print("\nInstallation failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
