#!/usr/bin/env python3
"""
🚀 ENHANCED AI MARKETING SYSTEM LAUNCHER
=========================================

Revolutionary launch script for the most advanced AI Marketing System.
Includes the new Master AI Orchestrator and Conversational Interface.

Features:
- Master AI Orchestrator with multi-agent conversations
- Revolutionary conversational UI
- Advanced agent personalities
- Real-time strategy generation
- Performance predictions
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path
from typing import Optional

# Define the project root directory, which is one level up from the 'launch' directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Add project root and key subdirectories to the Python path
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / 'src'))
sys.path.insert(0, str(PROJECT_ROOT / 'app'))

# Import the main application factory function now that paths are set
from gradio_app_enhanced import create_enhanced_gradio_interface

def print_header():
    """Print the enhanced system header"""
    print("""
    \033[35m
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║      🧠 AI MARKETING SYSTEM - REVOLUTIONARY EDITION 🚀          ║
    ║                                                                  ║
    ║    ✨ Master AI Orchestrator                                     ║ 
    ║    🎭 Multi-Agent Conversations                                  ║
    ║    💬 Conversational UI                                          ║
    ║    🎯 Predictive Analytics                                       ║
    ║    🚀 Enterprise-Ready Architecture                              ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    \033[0m
    """)

def check_environment():
    """Check if the environment is properly configured"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 8):
        print(f"❌ Python 3.8+ is required. Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} is compatible.")
    
    # Check for required files using paths relative to PROJECT_ROOT
    required_files = [
        PROJECT_ROOT / "src/core/master_orchestrator.py",
        PROJECT_ROOT / "src/ui/conversational_interface.py",
        PROJECT_ROOT / "config/.env"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not file_path.exists():
            missing_files.append(str(file_path.relative_to(PROJECT_ROOT)))
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    
    # Check .env configuration in the 'config' directory
    env_path = PROJECT_ROOT / "config" / ".env"
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=env_path)
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key and "your_" not in groq_api_key:
            print("✅ API keys configured")
        else:
            print("⚠️  GROQ_API_KEY not found or is a placeholder in .env")
            return False
    else:
        print(f"❌ .env file not found at {env_path}")
        return False
    
    return True

def install_enhanced_requirements():
    """Install enhanced system requirements"""
    print("📦 Installing enhanced system requirements...")
    
    enhanced_packages = [
        "gradio>=4.15.0",
        "groq>=0.4.1", 
        "python-dotenv>=1.1.1",
        "asyncio",
        "pydantic>=2.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0"
    ]
    
    try:
        for package in enhanced_packages:
            print(f"  📦 Installing {package}...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package, "--quiet"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        print("✅ Enhanced requirements installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def test_master_orchestrator():
    """Test the Master AI Orchestrator"""
    print("🧠 Testing Master AI Orchestrator...")
    
    try:
        # Add src to path
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        from src.core.master_orchestrator import MasterAIOrchestrator
        
        # Quick initialization test
        orchestrator = MasterAIOrchestrator()
        print("✅ Master AI Orchestrator initialized successfully!")
        
        # Test agent personalities
        if len(orchestrator.agent_personalities) >= 4:
            print("✅ AI Agent personalities loaded")
        else:
            print("⚠️  Some agent personalities missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Master AI Orchestrator test failed: {e}")
        return False

def launch_main_app():
    """Directly launch the main Gradio application in the same process."""
    print("🚀 Launching the AI Marketing System Application...")
    
    try:
        print("\n" + "="*80)
        print("🚀 AI MARKETING CONVERSATION STUDIO IS STARTING!")
        print("="*80)
        
        # Create the Gradio interface instance
        interface = create_enhanced_gradio_interface()
        
        print("✅ Enhanced system ready!")
        print("🔗 Opening at: http://127.0.0.1:7860")
        print("🛑 Press Ctrl+C in this terminal to stop the server.")
        print("="*80)
        
        # Launch the interface
        interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            inbrowser=True
        )

    except Exception as e:
        print(f"❌ Failed to launch the main application: {e}")
        import traceback
        traceback.print_exc()


def show_feature_overview():
    """Show the new features overview"""
    print("""
    🚀 NEW REVOLUTIONARY FEATURES:
    
    🧠 MASTER AI ORCHESTRATOR
    ├── Multi-agent strategic meetings
    ├── Human-like reasoning and collaboration  
    ├── Advanced campaign analysis
    └── Predictive performance modeling
    
    💬 CONVERSATIONAL INTERFACE
    ├── Natural language campaign creation
    ├── Chat-like interface with AI agents
    ├── Real-time strategy development
    └── Live performance predictions
    
    🎭 AI AGENT PERSONALITIES
    ├── Alexandra Sterling (AI Marketing CEO)
    ├── Marcus Chen (AI Marketing Director)
    ├── Sofia Rodriguez (AI Creative Director)
    └── David Kim (AI Performance Manager)
    
    📊 ENHANCED CAPABILITIES
    ├── Real-time trend analysis
    ├── Multi-platform optimization
    ├── A/B testing suggestions
    └── ROI predictions
    """)

def main():
    """Main launcher function"""
    print_header()
    
    # Show new features
    show_feature_overview()
    
    # Environment checks
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        return
    
    # Install requirements
    print("\n" + "="*50)
    print("SYSTEM PREPARATION")
    print("="*50)
    
    if not install_enhanced_requirements():
        print("❌ Failed to install requirements.")
        return
    
    # Test core components
    print("\n" + "="*50)
    print("SYSTEM TESTING")
    print("="*50)
    
    if not test_master_orchestrator():
        print("⚠️  Master AI Orchestrator test failed, but continuing...")
    
    # Launch interface
    print("\n" + "="*50)
    print("SYSTEM LAUNCH")
    print("="*50)
    
    try:
        launch_main_app()
    except KeyboardInterrupt:
        print("\n\n✅ System stopped by user")
        print("Thank you for using the AI Marketing System!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
