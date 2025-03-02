"""
Tests for init_ollama.py
"""
import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Create mock modules
ollama_mock = MagicMock()

# Mock the imports before importing init_ollama
with patch.dict(sys.modules, {
    'ollama': ollama_mock
}):
    import init_ollama

@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset all mocks before each test"""
    ollama_mock.reset_mock()
    yield

@pytest.fixture
def mock_ollama():
    """Mock ollama module"""
    with patch.dict(sys.modules, {
        'ollama': ollama_mock
    }):
        yield ollama_mock

@pytest.fixture
def mock_env():
    """Mock environment variables"""
    original_env = dict(os.environ)
    yield
    os.environ.clear()
    os.environ.update(original_env)

def test_ollama_host_from_env(mock_env):
    """Test OLLAMA_HOST is correctly read from environment"""
    test_host = "http://test-host:11434"
    os.environ["OLLAMA_HOST"] = test_host
    
    # Reload module to pick up new environment
    import importlib
    importlib.reload(init_ollama)
    
    assert init_ollama.OLLAMA_HOST == test_host

def test_ollama_host_default(mock_env):
    """Test OLLAMA_HOST default value"""
    if "OLLAMA_HOST" in os.environ:
        del os.environ["OLLAMA_HOST"]
    
    # Reload module to pick up new environment
    import importlib
    importlib.reload(init_ollama)
    
    assert init_ollama.OLLAMA_HOST == "http://localhost:11434"

@pytest.mark.asyncio
async def test_wait_for_ollama_success(mock_ollama):
    """Test successful connection to Ollama"""
    mock_models = MagicMock()
    mock_models.models = [MagicMock(), MagicMock()]  # Two mock models
    ollama_mock.list.return_value = mock_models
    
    assert init_ollama.wait_for_ollama() is True
    ollama_mock.list.assert_called_once()

@pytest.mark.asyncio
async def test_wait_for_ollama_eventual_success(mock_ollama):
    """Test connection to Ollama succeeds after retries"""
    mock_models = MagicMock()
    mock_models.models = [MagicMock()]
    
    # Fail twice, then succeed
    ollama_mock.list.side_effect = [
        Exception("Connection failed"),
        Exception("Still failed"),
        mock_models
    ]
    
    with patch('time.sleep') as mock_sleep:  # Don't actually sleep in tests
        assert init_ollama.wait_for_ollama() is True
    
    assert ollama_mock.list.call_count == 3
    assert mock_sleep.call_count == 2

@pytest.mark.asyncio
async def test_wait_for_ollama_failure(mock_ollama):
    """Test connection to Ollama fails after max retries"""
    ollama_mock.list.side_effect = Exception("Connection failed")
    
    with patch('time.sleep') as mock_sleep:  # Don't actually sleep in tests
        assert init_ollama.wait_for_ollama() is False
    
    assert ollama_mock.list.call_count == 30  # Max retries
    assert mock_sleep.call_count == 29

@pytest.mark.asyncio
async def test_init_models_connection_failure(mock_ollama):
    """Test init_models exits when connection fails"""
    ollama_mock.list.side_effect = Exception("Connection failed")
    
    with patch('time.sleep'), pytest.raises(SystemExit) as exc_info:
        await init_ollama.init_models()
    
    assert exc_info.value.code == 1

@pytest.mark.asyncio
async def test_init_models_all_installed(mock_ollama):
    """Test when all required models are already installed"""
    # Create mock models that match all required models
    mock_models = MagicMock()
    mock_models.models = []
    for model_name in init_ollama.REQUIRED_MODELS:
        model = MagicMock()
        model.model = model_name
        mock_models.models.append(model)
    
    ollama_mock.list.return_value = mock_models
    
    await init_ollama.init_models()
    
    # Should not attempt to pull any models
    ollama_mock.pull.assert_not_called()

@pytest.mark.asyncio
async def test_init_models_pull_new(mock_ollama):
    """Test pulling models that aren't installed"""
    # Create mock models with only one installed
    mock_models = MagicMock()
    mock_models.models = [MagicMock()]
    mock_models.models[0].model = init_ollama.REQUIRED_MODELS[0]
    
    ollama_mock.list.return_value = mock_models
    
    await init_ollama.init_models()
    
    # Should attempt to pull missing models
    assert ollama_mock.pull.call_count == len(init_ollama.REQUIRED_MODELS) - 1

@pytest.mark.asyncio
async def test_init_models_pull_failure(mock_ollama):
    """Test handling of model pull failure"""
    # Create mock models with none installed
    mock_models = MagicMock()
    mock_models.models = []
    ollama_mock.list.return_value = mock_models
    
    # Make pull fail
    ollama_mock.pull.side_effect = Exception("Pull failed")
    
    with pytest.raises(SystemExit) as exc_info:
        await init_ollama.init_models()
    
    assert exc_info.value.code == 1
    assert ollama_mock.pull.call_count == 1  # Should fail on first pull

@pytest.mark.asyncio
async def test_main_execution():
    """Test script execution through main"""
    with patch('asyncio.run') as mock_run:
        # Set __name__ to '__main__' to trigger the main block
        original_name = init_ollama.__name__
        try:
            init_ollama.__name__ = '__main__'
            # Re-execute the main block
            exec(open(init_ollama.__file__).read())
        finally:
            init_ollama.__name__ = original_name
        
        mock_run.assert_called_once_with(init_ollama.init_models()) 