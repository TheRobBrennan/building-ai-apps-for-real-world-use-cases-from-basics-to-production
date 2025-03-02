"""
Quick verification of required packages for AI Basics workshop.
This is a temporary file that will be replaced during the workshop.
"""

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
        import jupyter
        packages.append(("jupyter", jupyter.__version__))
    except ImportError:
        packages.append(("jupyter", "NOT FOUND"))
    
    return packages

def main():
    print("AI Basics Workshop - Package Verification")
    print("----------------------------------------")
    packages = verify_dependencies()
    
    all_found = True
    for package, version in packages:
        status = "✅" if version != "NOT FOUND" else "❌"
        print(f"{status} {package}: {version}")
        if version == "NOT FOUND":
            all_found = False
    
    if all_found:
        print("\n✨ All required packages are installed!")
    else:
        print("\n⚠️  Some packages are missing. Please run:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main() 