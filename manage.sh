#!/bin/bash

# Ensure the script exits if any command fails
set -e

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

# Default to this application if no environment variables are provided
# Experiment 0: The obligatory "Hello, world!" example
: ${APP_DIR:="apps/hello_world"}
: ${APP_SCRIPT:="hello_world.py"}

# Define the directory for the virtual environment
VENV_DIR=".venv"

# Change to the specified directory
cd $APP_DIR

# Function to set up the virtual environment
setup_venv() {
    # Check if the virtual environment already exists
    if [[ ! -d "$VENV_DIR" ]]; then
        python3 -m venv "$VENV_DIR"
        # Activate the virtual environment
        source "$VENV_DIR/bin/activate"

        # Upgrade pip
        pip install --upgrade pip

        # Install test dependencies
        pip install pytest pytest-cov

        # Install dependencies only if requirements.txt exists
        if [[ -f "requirements.txt" ]]; then
            pip install -r requirements.txt
        else
            echo "No requirements.txt found. Skipping dependency installation."
        fi

        # Deactivate the virtual environment
        deactivate
    fi
}

# Function to start the application
run_app() {
    # Ensure the virtual environment is set up
    setup_venv

    # Activate the virtual environment
    source "$VENV_DIR/bin/activate"

    # Run the app
    python3 $APP_SCRIPT

    # Deactivate the virtual environment
    # deactivate
}

# Function to run pytest tests
run_tests() {
    # Ensure the virtual environment is set up
    setup_venv

    # Activate the virtual environment
    source "$VENV_DIR/bin/activate"

    # Check if there are any Python test files
    if ls test_*.py 1> /dev/null 2>&1 || ls */test_*.py 1> /dev/null 2>&1; then
        # Check for coverage flag
        if [[ "$1" == "--coverage" ]]; then
            pytest --cov=. --cov-config=.coveragerc --cov-report=html && open htmlcov/index.html
        else
            pytest
        fi
    else
        echo "No Python tests found in current directory."
    fi

    # Deactivate the virtual environment
    deactivate

    # Return to root directory to run GitHub workflow tests
    cd - > /dev/null
    echo -e "\nRunning GitHub workflow tests..."
    npm run test:github
}

# Function to destroy the virtual environment
destroy_venv() {
    if [[ -d "$VENV_DIR" ]]; then
        rm -rf "$VENV_DIR"
        echo "Virtual environment '$VENV_DIR' has been removed."
    else
        echo "Virtual environment '$VENV_DIR' does not exist."
    fi
}

# Main execution
case $1 in
    "setup")
        setup_venv
        run_app
        ;;
    "start")
        run_app
        ;;
    "test")
        run_tests $2
        ;;
    "destroy")
        destroy_venv
        ;;
    *)
        echo "Usage: $0 {setup|start|test [--coverage]}"
        exit 1
esac
