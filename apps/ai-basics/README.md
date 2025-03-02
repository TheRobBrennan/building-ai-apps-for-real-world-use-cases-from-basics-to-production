# AI Basics Workshop

This directory contains the code and resources for the AI Basics workshop by Ravin Kumar and Hugo Bowne Anderson.

## Prerequisites

### Required Packages

- numpy
- ollama
- gradio
- jupyter

### Required Ollama Models

- gemma2:2b (Base model)
- gemma2:2b-instruct-fp16 (Instruction-tuned model with FP16 precision)
- gemma2:2b-instruct-q2_K (Quantized instruction-tuned model)

Note: The Gemma models require approximately 10GB of disk space.

## Quick Start

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Install Ollama models:

   ```bash
   ollama pull gemma2:2b
   ollama pull gemma2:2b-instruct-fp16
   ollama pull gemma2:2b-instruct-q2_K
   ```

3. Verify your setup:

   ```bash
   python verify_environment.py
   ```

   This will check that all required packages and models are properly installed.

### Example Outputs

#### Successful Environment Check

```
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

#### Missing Dependencies Example

```
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

## Troubleshooting

If the verification script shows missing requirements:

1. For missing Python packages: Run `pip install -r requirements.txt`
2. For missing Ollama models: Run the `ollama pull` commands shown in the verification output
3. Ensure Ollama is running on your system

### Installation Times and Sizes

Model installation times and sizes from a sample run:

- gemma2:2b: 31 seconds, 1.5GB
- gemma2:2b-instruct-fp16: 79 seconds, 4.9GB
- gemma2:2b-instruct-q2_K: 25 seconds, 1.1GB

Total installation time: ~2 minutes 15 seconds
Total disk space: ~7.5GB
