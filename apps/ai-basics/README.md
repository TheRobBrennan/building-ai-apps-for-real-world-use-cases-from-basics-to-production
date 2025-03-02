# AI Basics Workshop

This directory contains the code and resources for the AI Basics workshop by Ravin Kumar and Hugo Bowne Anderson.

## Prerequisites

### Required Packages

- numpy
- ollama
- gradio
- jupyter

### Required Ollama Models

- gemma:2b (Base model)
- gemma:2b-instruct (Instruction-tuned model)
- gemma:2b-instruct-q4_0 (Quantized instruction-tuned model)

Note: The Gemma models require approximately 10GB of disk space.

## Quick Start

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Install Ollama models:

   ```bash
   ollama pull gemma:2b
   ollama pull gemma:2b-instruct
   ollama pull gemma:2b-instruct-q4_0
   ```

3. Verify your setup:

   ```bash
   python verify_environment.py
   ```

   This will check that all required packages and models are properly installed.

## Project Structure

- `verify_environment.py` - Script to verify your local development environment
- `requirements.txt` - Python package dependencies
- Additional files will be added during the workshop

## Troubleshooting

If the verification script shows missing requirements:

1. For missing Python packages: Run `pip install -r requirements.txt`
2. For missing Ollama models: Run the `ollama pull` commands shown in the verification output
3. Ensure Ollama is running on your system
