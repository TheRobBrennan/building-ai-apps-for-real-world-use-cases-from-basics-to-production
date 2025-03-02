"""
Initialize required Ollama models.
"""
import asyncio
import sys
import time
import os
import ollama

# Get Ollama host from environment or use default
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
print(f"Using Ollama host: {OLLAMA_HOST}")

REQUIRED_MODELS = [
    "gemma2:2b",
    "gemma2:2b-instruct-fp16",
    "gemma2:2b-instruct-q2_K"
]

def wait_for_ollama():
    """Wait for Ollama service to be ready."""
    max_retries = 30
    retry_interval = 2
    
    for i in range(max_retries):
        try:
            print(f"Attempting to connect to Ollama at {OLLAMA_HOST}...")
            models = ollama.list()
            print("✅ Ollama service is ready")
            print(f"Found {len(models.models)} models")
            return True
        except Exception as e:
            if i < max_retries - 1:
                print(f"Waiting for Ollama service (attempt {i + 1}/{max_retries})")
                print(f"Error: {str(e)}")
                time.sleep(retry_interval)
            else:
                print(f"❌ Failed to connect to Ollama service: {e}")
                return False

async def init_models():
    """Initialize required Ollama models."""
    if not wait_for_ollama():
        sys.exit(1)
    
    print("\nChecking and pulling required models...")
    
    # Get list of installed models
    models = ollama.list()
    installed_models = {model.model for model in models.models}
    
    # Pull missing models
    for model in REQUIRED_MODELS:
        if model not in installed_models:
            print(f"Pulling {model}...")
            try:
                ollama.pull(model)
                print(f"✅ Successfully pulled {model}")
            except Exception as e:
                print(f"❌ Failed to pull {model}: {e}")
                sys.exit(1)
        else:
            print(f"✅ Model {model} is already installed")
    
    print("\n✨ All required models are ready!")

if __name__ == "__main__":
    asyncio.run(init_models()) 