# Building AI Apps for Real World Use Cases

This repository contains practical AI applications and examples, focusing on real-world implementation and best practices.

## Projects

### AI Basics

Located in `apps/ai-basics/`, this project follows the tutorial by Ravin Kumar and Hugo Bowne Anderson, exploring the fundamentals of building AI applications.

#### Prerequisites

- [Ollama](https://ollama.com/) installed locally (for local setup)
- Python 3.x (for local setup)
- Virtual environment management (via `manage.sh`) (for local setup)
- Docker and Docker Compose (for Docker setup)

#### Required Gemma Models

You'll need to pull the following models:

```bash
ollama pull gemma2:2b
ollama pull gemma2:2b-instruct-fp16
ollama pull gemma2:2b-instruct-q2_K
```

Note: These models require approximately 10GB of disk space.

## Development Setup

You can run this project either locally or using Docker.

### Using Docker (Recommended)

The following npm scripts are available for Docker-based development:

- `npm run docker:build` - Build the Docker image
- `npm run docker:start` - Run the application
- `npm run docker:test` - Run tests in Docker
- `npm run docker:test:coverage` - Run tests with coverage in Docker
- `npm run docker:clean` - Clean up Docker resources

### Local Setup

#### Environment Management

The `manage.sh` script provides several utility commands:

- `./manage.sh setup` - Creates virtual environment and installs dependencies
- `./manage.sh start` - Activates environment and runs the specified application
- `./manage.sh test` - Runs tests (use `--coverage` flag for coverage report)
- `./manage.sh destroy` - Removes virtual environment

### Project Configuration

1. Copy `.env.sample` to `.env`
2. Update the environment variables:

   ```sh
   APP_DIR=apps/your_project_directory
   APP_SCRIPT=your_main_script.py
   ```

### Project Structure

```txt
apps/
  └── project_directory/
      ├── main_script.py
      ├── requirements.txt
      └── other_files.py
```

### For JavaScript Developers

NPM scripts are available as wrappers around `manage.sh`:

- `npm run setup` - Set up environment
- `npm run start` - Start application
- `npm run test` - Run tests
- `npm run test:coverage` - Run tests with coverage
- `npm run destroy` - Clean up environment

## Python Development Guide

### Virtual Environment Commands

```sh
# Create virtual environment
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate requirements.txt
pip freeze > requirements.txt

# Deactivate
deactivate
```

## Testing GitHub Actions

We use [act](https://github.com/nektos/act) for testing GitHub Actions locally.

Prerequisites:

- Homebrew
- Docker Desktop (running)

```sh
# Install act
brew install act

# Verify installation
act --version  # Should show 0.2.74 or higher
```

### Available Test Scripts

- `npm run test:github` - Run all workflow tests
- `npm run test:workflows` - Test PR validation and version bumping
- `npm run test:workflows:semantic[:major|:minor|:patch]` - Test specific PR formats
- `npm run test:workflows:version` - Test version bump workflow
- `npm run test:workflows:merge` - Test merge workflow

## Development Guidelines

- **Version Control**: Semantic versioning with automated version bumps
- **Commit Signing**: All commits must be GPG signed
- **Pull Requests**: Follow conventional commit format

For detailed guidelines, see:

- [Contributing Guidelines](./CONTRIBUTING.md)
- [Testing Documentation](./.github/docs/TESTING.md)
- [Repository Setup](./.github/docs/SETUP.md)
