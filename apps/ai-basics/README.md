# AI Basics Workshop

This directory contains the code and resources for the AI Basics workshop by Ravin Kumar and Hugo Bowne Anderson.

## Prerequisites

You can run this project either locally or using Docker.

### Local Setup

#### Required Tools

- UV (Python package manager)
- Ollama (for running AI models locally)

#### Required Python Packages

- numpy
- ollama
- gradio
- jupyter

#### Required Ollama Models

- gemma2:2b (Base model)
- gemma2:2b-instruct-fp16 (Instruction-tuned model with FP16 precision)
- gemma2:2b-instruct-q2_K (Quantized instruction-tuned model)

Note: The Gemma models require approximately 10GB of disk space.

### Docker Setup

If you prefer using Docker, you'll need:

- Docker
- Docker Compose

## Quick Start

### Using Docker (Recommended)

1. Build the Docker image:

   ```bash
   npm run docker:build
   ```

2. Run the application:

   ```bash
   npm run docker:start
   ```

3. Run tests:

   ```bash
   npm run docker:test
   ```

4. Run tests with coverage:

   ```bash
   npm run docker:test:coverage
   ```

5. Clean up Docker resources:

   ```bash
   npm run docker:clean
   ```

### Local Development Steps

1. Install UV:

   ```bash
   pip install uv
   ```

2. Create and activate a virtual environment:

   ```bash
   # Create environment
   uv venv .venv

   # Activate environment
   # On macOS/Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   uv pip install -r requirements.txt
   ```

4. Install Ollama models:

   ```bash
   ollama pull gemma2:2b
   ollama pull gemma2:2b-instruct-fp16
   ollama pull gemma2:2b-instruct-q2_K
   ```

5. Verify your setup:

   ```bash
   python verify_environment.py
   ```

   This will check that all required packages and models are properly installed.

## Example Outputs

### Successful Verification

```console
==================================================
AI Basics Workshop - Package Verification
==================================================

Checking required packages...
✅ numpy: 2.2.3
✅ ollama: installed
✅ gradio: 5.20.0
✅ jupyter: 5.7.2

Checking required Ollama models...
✅ gemma2:2b (1.5GB)
✅ gemma2:2b-instruct-fp16 (4.9GB)
✅ gemma2:2b-instruct-q2_K (1.1GB)

✨ All requirements are satisfied!

==================================================
```

### Missing Dependencies Example

```console
==================================================
AI Basics Workshop - Package Verification
==================================================

Checking required packages...
✅ numpy: 2.2.3
❌ ollama: NOT FOUND
✅ gradio: 5.20.0
❌ jupyter: NOT FOUND

Checking required Ollama models...
❌ gemma2:2b
❌ gemma2:2b-instruct-fp16
❌ gemma2:2b-instruct-q2_K

⚠️  Some requirements are missing:
- Install missing packages: pip install -r requirements.txt
- Install missing models:
  ollama pull gemma2:2b
  ollama pull gemma2:2b-instruct-fp16
  ollama pull gemma2:2b-instruct-q2_K

==================================================
```

## Project Structure

- `verify_environment.py` - Script to verify your local development environment
- `requirements.txt` - Python package dependencies
- Additional files will be added during the workshop

## Troubleshooting Guide

If the verification script shows missing requirements:

1. For missing Python packages: Run `pip install -r requirements.txt`
2. For missing Ollama models: Run the `ollama pull` commands shown in the verification output
3. Ensure Ollama is running on your system

### Installation Metrics

Model installation times and sizes from a sample run:

- gemma2:2b: 31 seconds, 1.5GB
- gemma2:2b-instruct-fp16: 79 seconds, 4.9GB
- gemma2:2b-instruct-q2_K: 25 seconds, 1.1GB

Total installation time: ~2 minutes 15 seconds
Total disk space: ~7.5GB
