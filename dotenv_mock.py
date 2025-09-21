"""Simple dotenv mock implementation"""
import os

def load_dotenv(path=None):
    """Mock load_dotenv function"""
    # Set some default environment variables for testing
    os.environ.setdefault("OPENROUTER_API_KEY", "optional")
    os.environ.setdefault("DEEPSEEK_API_KEY", "optional") 
    os.environ.setdefault("GEMINI_API_KEY", "optional")
    os.environ.setdefault("CLAUDE_API_KEY", "optional")
    return True