#!/usr/bin/env python3
"""
Simple Package Installer for AI Marketing System
================================================

This script installs packages one by one to avoid dependency conflicts.
"""

import subprocess
import sys

def install_package(package_name):
    """Install a single package."""
    try:
        print(f"📦 Installing {package_name}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package_name, "--user"
        ])
        print(f"✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        return False

def main():
    """Main installation function."""
    print("🤖 AI Marketing System - Package Installer")
    print("=" * 50)
    
    # Core packages in order of importance
    packages = [
        "python-dotenv",
        "requests", 
        "groq",
        "gradio",
        "openai",
        "pydantic",
        "sqlalchemy"
    ]
    
    successful = []
    failed = []
    
    # Upgrade pip first
    print("🔧 Upgrading pip...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--user"
        ])
        print("✅ Pip upgraded successfully")
    except Exception as e:
        print(f"⚠️ Pip upgrade failed: {e}")
    
    # Install packages one by one
    for package in packages:
        if install_package(package):
            successful.append(package)
        else:
            failed.append(package)
        print()  # Add spacing
    
    # Summary
    print("=" * 50)
    print("📊 Installation Summary:")
    print(f"✅ Successfully installed: {len(successful)} packages")
    for pkg in successful:
        print(f"   • {pkg}")
    
    if failed:
        print(f"❌ Failed to install: {len(failed)} packages")
        for pkg in failed:
            print(f"   • {pkg}")
    
    print("=" * 50)
    
    if len(successful) >= 4:  # At least the core packages
        print("🎉 Core packages installed! You can now run the system.")
        print("Run: python launch.py")
    else:
        print("⚠️ Too many packages failed. Please check your Python environment.")

if __name__ == "__main__":
    main()
