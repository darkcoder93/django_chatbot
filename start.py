#!/usr/bin/env python3
"""
Quick startup script for the SQL Chatbot Django application.
This script helps you get the application running quickly.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import django
        import rest_framework
        import pandas
        import openpyxl
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: uv sync")
        return False


def check_env_file():
    """Check if .env file exists"""
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("Creating .env file from template...")
        
        # Copy from env.example if it exists
        example_file = Path('env.example')
        if example_file.exists():
            with open(example_file, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print("✅ Created .env file from template")
            print("⚠️  Please update .env file with your actual configuration")
        else:
            print("❌ env.example file not found")
            print("Please create a .env file manually")
        return False


def run_migrations():
    """Run Django migrations"""
    try:
        print("🔄 Running database migrations...")
        subprocess.run(['uv', 'run', 'python', 'manage.py', 'migrate'], check=True)
        print("✅ Database migrations completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        return False


def start_server():
    """Start the Django development server"""
    try:
        print("🚀 Starting Django development server...")
        print("📱 Open your browser and go to: http://127.0.0.1:8000/")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        subprocess.run(['uv', 'run', 'python', 'manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")


def main():
    """Main startup function"""
    print("🤖 SQL Chatbot - Django Application")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check environment file
    check_env_file()
    
    # Run migrations
    if not run_migrations():
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Update .env file with your OpenAI API key")
    print("2. Configure your database settings if needed")
    print("3. The server will start automatically")
    
    # Start server
    start_server()


if __name__ == "__main__":
    main() 