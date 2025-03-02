"""
Quick verification of required packages for AI Basics workshop.
This is a temporary file that will be replaced during the workshop.
"""
import asyncio
import sys

def verify_dependencies():
    packages = []
    
    try:
        import numpy as np
        packages.append(("numpy", np.__version__))
    except ImportError:
        packages.append(("numpy", "NOT FOUND"))
    
    try:
        import ollama
        # Ollama doesn't expose version in a standard way
        packages.append(("ollama", "installed"))
    except ImportError:
        packages.append(("ollama", "NOT FOUND"))
    
    try:
        import gradio as gr
        packages.append(("gradio", gr.__version__))
    except ImportError:
        packages.append(("gradio", "NOT FOUND"))
    
    try:
        import jupyter_core
        packages.append(("jupyter", jupyter_core.__version__))
    except ImportError:
        packages.append(("jupyter", "NOT FOUND"))
    
    return packages

async def verify_ollama_models():
    required_models = [
        "gemma:2b",
        "gemma:2b-instruct",
        "gemma:2b-instruct-q4_0"
    ]
    model_status = []
    
    try:
        import ollama
        # Get list of installed models
        models = ollama.list()
        installed_models = [model.model for model in models.models]
        
        for model in required_models:
            if model in installed_models:
                model_status.append((model, "installed"))
            else:
                model_status.append((model, "NOT FOUND"))
    except ImportError:
        # If ollama package isn't installed, mark all models as not found
        for model in required_models:
            model_status.append((model, "NOT FOUND"))
    except Exception as e:
        # If we can't get the model list, mark all as not found
        print(f"\nWarning: Could not check Ollama models: {str(e)}")
        for model in required_models:
            model_status.append((model, "NOT FOUND"))
    
    return model_status

def main():
    print("\n" + "="*50)
    print("AI Basics Workshop - Package Verification")
    print("="*50 + "\n")
    
    # Check package dependencies
    print("Checking required packages...")
    packages = verify_dependencies()
    
    all_packages_found = True
    for package, version in packages:
        status = "✅" if version != "NOT FOUND" else "❌"
        print(f"{status} {package}: {version}")
        if version == "NOT FOUND":
            all_packages_found = False
    
    # Check Ollama models
    print("\nChecking required Ollama models...")
    model_status = asyncio.run(verify_ollama_models())
    
    all_models_found = True
    for model, status in model_status:
        icon = "✅" if status == "installed" else "❌"
        print(f"{icon} {model}")
        if status != "installed":
            all_models_found = False
    
    # Print summary
    if all_packages_found and all_models_found:
        print("\n✨ All requirements are satisfied!")
    else:
        print("\n⚠️  Some requirements are missing:")
        if not all_packages_found:
            print("- Install missing packages: pip install -r requirements.txt")
        if not all_models_found:
            print("- Install missing models:")
            for model, status in model_status:
                if status != "installed":
                    print(f"  ollama pull {model}")
    
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main() 