# Welcome

This project will explore getting started developing with [Python](https://www.python.org) as quickly as possible using ~~[Visual Studio Code](https://code.visualstudio.com)~~ [Cursor](https://www.cursor.com).

## Local development

If you are using Python for development, the `manage.sh` script provides several utility commands to streamline common tasks:

- `./manage.sh setup` - **Set up the environment and start the application:** This command prepares the development environment by creating a virtual environment in the `.venv` directory (if it doesn't exist). If a `requirements.txt` file is present in the specified app directory (default is `apps/hello_world`), the dependencies listed will be installed. After setting up the environment, the application script (default is `hello_world.py`) is executed.
- `./manage.sh start` - **Start the application:** This command ensures that the virtual environment is set up, activates it, and then runs the specified application script. After execution, the virtual environment is deactivated.
- `./manage.sh test` - **Run tests:** This command ensures that the virtual environment is set up and then runs the tests using pytest. If you want to test with coverage, use the `--coverage` flag.
- `./manage.sh test --coverage` - **Run tests with coverage:** This command runs all tests and generates a coverage report. The report is generated in the `htmlcov` directory, and the index page of the report is automatically opened in your default browser.
- `./manage.sh destroy` - **Clean up the environment:** This command removes the `.venv` virtual environment, effectively deleting all the installed packages and configurations. It's useful when you want to reset your development environment.

Please copy `.env.sample` to `.env` to specify a folder and initial file for the main script to run.

### Configuring Your Python Project

By default, this project is set up to run the "Hello, world!" example located at `apps/hello_world/hello_world.py`. If you want to use your own Python project, you have two options:

1. **Edit the `.env` file (Recommended):**
   - Copy `.env.sample` to `.env` if you haven't already
   - Update the following variables in the `.env` file:

     ```sh
     APP_DIR=apps/your_project_directory
     APP_SCRIPT=your_main_script.py
     ```

   - This is the preferred method as it persists your configuration

2. **Use environment variables when running commands:**

   ```sh
   APP_DIR="apps/your_project_directory" APP_SCRIPT="your_main_script.py" ./manage.sh start
   ```

The `manage.sh` script will use these values to locate and run your Python application. Make sure your project directory contains a `requirements.txt` file if you have dependencies that need to be installed.

#### Project Structure

When adding your own Python project, we recommend following this structure:

```txt
apps/
  └── your_project_directory/
      ├── your_main_script.py
      ├── requirements.txt
      └── other_files.py
```

This keeps your project organized and allows the `manage.sh` script to find and manage your dependencies correctly.

### For JavaScript Developers

If you're more familiar with JavaScript development and have `npm` installed, we've made it easier for you to work with this Python project. There are several helper scripts defined in the `package.json` file which are wrappers around the above `manage.sh` commands:

- `npm run setup` - Sets up the environment and starts the application. Equivalent to `./manage.sh setup`.

- `npm run start` - Starts the application. Equivalent to `./manage.sh start`.

- `npm run test` - Runs all tests. Equivalent to `./manage.sh test`.

- `npm run test:coverage` - Runs tests and generates a coverage report. Equivalent to `./manage.sh test --coverage`.

- `npm run destroy` - Cleans up the environment by removing the virtual environment. Equivalent to `./manage.sh destroy`.

- `npm repo` - Opens the project repository in your default browser. This is a quick way to access the source code, documentation, and other related resources.

Utilizing these npm scripts, you can manage the Python application using commands you're familiar with from the JavaScript ecosystem.

### EXAMPLE: Hello, world

What project starter would be complete without an obligatory "Hello, world!" example? 🤓

```sh
(.venv) hello-world % python3 hello_world.py 
Hello, world!
```

## Python cheat sheet

If you're just getting started with Python, here are snippets of commands that you may find helpful to get you up and running in no time.

```sh
# Verify that you have Python installed on your machine
% python3 --version
Python 3.13.1

# Create a new virtual environment for the project
% python3 -m venv .venv

# Select your new environment by using the Python: Select Interpreter command in VS Code
#   - Enter the path: ./.venv/bin/python

# Activate your virtual environment
% source .venv/bin/activate
(.venv) %

# PREFERRED: Install the packages from requirements.txt
(.venv) % pip install -r requirements.txt

# Install Python packages in a virtual environment
# (.venv) % pip install <package_name>

# Install Python testing packages
# (.venv) % pip install pytest pytest-asyncio
# (.venv) % pip install pytest-cov

# When you are ready to generate a requirements.txt file
# (.venv) % pip freeze > requirements.txt

# Uninstall the package from your virtual environment
# (.venv) % pip uninstall simplejson

# Remove the dependency from requirements.txt if it exists
# (.venv) % pip uninstall -r requirements.txt

# To run unit tests:
# (.venv) % pytest

# To run unit tests and automatically view the HTML coverage report on macOS:
# (.venv) % pytest --cov=. --cov-report=html && open htmlcov/index.html

# To run a single unit test
# (.venv) % pytest test_something.py

# Deactivate your virtual environment
(.venv) % deactivate
% 

```

## Testing GitHub Actions Locally

We recommend using [act](https://github.com/nektos/act) to test GitHub Actions workflows locally before pushing changes if you are developing on a Mac.

The application does not have to be running in Docker to test the workflows, but Docker Desktop must be running for the act tests to run and spin up the necessary containers.

Prerequisites for macOS

- Homebrew
- Docker Desktop (must be running)

```sh
# Install act using Homebrew
brew install act

# Verify installation
act --version # Should show 0.2.74 or higher

```

### Running Tests

The following test scripts are available:

1. `npm run test:github`
   - Primary test command for GitHub Actions
   - Runs all workflow tests via test:workflows
   - Recommended for testing GitHub Actions workflows

2. `npm run test:workflows`
   - Runs all workflow tests in sequence
   - Tests PR title validation and version bumping
   - Provides detailed feedback

3. `npm run test:workflows:semantic`
   - Tests PR title validation only (using minor version example)
   - Validates against conventional commit format

4. `npm run test:workflows:semantic:major`
   - Tests PR title validation with breaking change
   - Validates major version bump detection

5. `npm run test:workflows:semantic:minor`
   - Tests PR title validation with new feature
   - Validates minor version bump detection

6. `npm run test:workflows:semantic:patch`
   - Tests PR title validation with bug fix
   - Validates patch version bump detection

7. `npm run test:workflows:semantic:invalid`
   - Tests PR title validation with invalid format
   - Verifies rejection of non-compliant PR titles

8. `npm run test:workflows:version`
   - Tests version bump workflow
   - Note: Git operations will fail locally (expected)

9. `npm run test:workflows:merge`
   - Tests main branch merge workflow
   - Simulates PR merge and version bump process
   - Note: Git operations will fail locally (expected)

#### Expected Test Results

1. Semantic PR Check Tests:
   - All tests should pass except "invalid" test
   - Invalid PR format test should fail with clear error

2. Version Bump Tests:
   - Will show git authentication errors (expected)
   - These workflows can only be fully tested in GitHub Actions

3. Merge Tests:
   - Will show authentication errors locally (expected)
   - Tests workflow syntax and merge logic
   - Full functionality requires GitHub Actions environment

## Development Guidelines

- **Version Control**: We use semantic versioning with automated version bumps
- **Commit Signing**: All commits must be GPG signed
- **Pull Requests**: PR titles must follow conventional commit format

For detailed guidelines, see:

- [Contributing Guidelines](./CONTRIBUTING.md)
- [Testing Documentation](./.github/docs/TESTING.md)
- [Repository Setup](./.github/docs/SETUP.md) (for maintainers)
